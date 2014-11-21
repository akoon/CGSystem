/*!
 * Extensible 1.5.1
 * Copyright(c) 2010-2011 Extensible, LLC
 * licensing@ext.ensible.com
 * http://ext.ensible.com
 */

Ext.Loader.setConfig({
    enabled: true,
    disableCaching: false,
    paths: {
        "Extensible": "/static/timesheet2/src"
        //"Extensible.example.calendar": "."
    }
});

Ext.define('Extensible.App', {
    
    requires: [
        'Ext.Viewport',
        'Ext.layout.container.Border',
        'Extensible.calendar.CalendarPanel',
        'Extensible.calendar.gadget.CalendarListPanel',
        'Extensible.calendar.gadget.TaskListPanel',
        'Extensible.calendar.data.MemoryCalendarStore',
        'Extensible.calendar.data.MemoryEventStore',
        'Extensible.calendar.data.MemoryTasksStore',
        'Extensible.calendar.data.Events',
        'Extensible.calendar.data.Calendars',
        'Extensible.calendar.data.TaskModel'
    ],
    
    constructor : function() {
        // This is an example calendar store that enables event color-coding
        this.calendarStore = Ext.create('Extensible.calendar.data.MemoryCalendarStore', {
            // defined in ../data/Calendars.js
            //data: Ext.create('Extensible.calendar.data.Calendars')
        	autoLoad: true,
        	proxy: {
				type: 'ajax',
				url: '/get_actual_status',
				reader: {
						type: 'json',
						root: 'status',
						successProperty: 'success'
				},
				method: 'GET'
			}
        });
		
        // A sample event store that loads static JSON from a local file. Obviously a real
        // implementation would likely be loading remote data via an HttpProxy, but the
        // underlying store functionality is the same.
        
        /*
        this.eventStore = Ext.create('Extensible.calendar.data.MemoryEventStore', {
            // defined in ../data/Events.js
            //Ext.create('Extensible.calendar.data.Events'),
            // This disables the automatic CRUD messaging built into the sample data store.
            // This test application will provide its own custom messaging. See the source
            // of MemoryEventStore to see how automatic store messaging is implemented.
            autoMsg: false
        });
        */
        
		//任务列表数据
		this.taskStore = Ext.create('Extensible.calendar.data.MemoryTasksStore');
		
		//daily数据
		this.dailyStore = Ext.create('Extensible.calendar.data.MemoryDailyStore');
//		console.log('this.dailyStore    ' + this.dailyStore);
		/*
		//task combobox数据
		this.taskComboStore = Ext.create('Extensible.calendar.data.MemoryTasksComboStore');
		
		//mission combobox数据
		this.missionComboStrore = Ext.create('Extensible.calendar.data.MemoryMissionsComboStore');
        */
        this.eventStore = Ext.create('Extensible.calendar.data.MemoryEventStore', {
		    autoLoad: true,
		    autoSync: true,
		    proxy: {
		        type: 'ajax',
		        api: {
					read: '/get_actual_tasks/' + Ext.get("user-id").dom.innerHTML,
					create: '/add_actual_task/' + Ext.get("user-id").dom.innerHTML,
					update: '/update_actual_task/' + Ext.get("user-id").dom.innerHTML,
					destroy: '/remove_actual_task/' + Ext.get("user-id").dom.innerHTML
				},
		        noCache: false,
		        successProperty: 'success',
		        reader: {
		            type: 'json',
		            root: 'tasks'
		        },
		        writer: {
		        	type: 'json',
		        	nameProperty: 'mapping'
		        },
		        
				listeners: {
		            exception: function(proxy, response, operation, options){
		                var msg = response.message ? response.message : Ext.decode(response.responseText).message;
		                // ideally an app would provide a less intrusive message display
		                var json = eval("(" + response.responseText + ")");
						console.log('json.success    ' + json.success);
						if(json.success == 'false')
						{
							Ext.MessageBox.alert('提示', json.msg);
						}
		                
		            }
            	}
		    },
		    
		    // It's easy to provide generic CRUD messaging without having to handle events on every individual view.
		    // Note that while the store provides individual add, update and remove events, those fire BEFORE the
		    // remote transaction returns from the server -- they only signify that records were added to the store,
		    // NOT that your changes were actually persisted correctly in the back end. The 'write' event is the best
		    // option for generically messaging after CRUD persistence has succeeded.
		    listeners: {
		        'write': function(store, operation){
		            //var title = Ext.value(operation.records[0].data[Extensible.calendar.data.EventMappings.Title.name], '(No title)');
		            switch(operation.action){
		                case 'create': 
		                    //Extensible.example.msg('Add', 'Added "' + title + '"');
		                    //console.log('event add function called aaaaaaaaaaaaaaa');	                    
		                    break;
		                case 'update':
		                    //Extensible.example.msg('Update', 'Updated "' + title + '"');
		                    //console.log('event update function called bbbbbbbbbbbbbbbbb');
		                    break;
		                case 'destroy':
		                    //Extensible.example.msg('Delete', 'Deleted "' + title + '"');
		                    //console.log('event del function called ccccccccccccccccccc');
		                    break;
		            }
		        }
		    }
		});
        //console.log('eventStore' + this.eventStore.data);
        
        // This is the app UI layout code.  All of the calendar views are subcomponents of
        // CalendarPanel, but the app title bar and sidebar/navigation calendar are separate
        // pieces that are composed in app-specific layout code since they could be omitted
        // or placed elsewhere within the application.
        Ext.create('Ext.Viewport', {
            layout: 'border',
            renderTo: 'calendar-ct',
            items: [{
                id: 'app-header',
                region: 'north',
                height: 30,
                border: false,
                contentEl: 'app-header-content'
            },{
                id: 'app-center',
                title: '...', // will be updated to the current view's date range
                region: 'center',
                layout: 'border',
                listeners: {
                    'afterrender': function(){
                        Ext.getCmp('app-center').header.addCls('app-center-header');
                    }
                },
                items: [{
                    id:'app-west',
                    region: 'west',
                    width: 179,
                    border: false,
                    items: [{
                        xtype: 'datepicker',
                        id: 'app-nav-picker',
                        cls: 'ext-cal-nav-picker',
                        listeners: {
                            'select': {
                                fn: function(dp, dt){
                                    Ext.getCmp('app-calendar').setStartDate(dt);
                                },
                                scope: this
                            }
                        }
                    },
                    	/*{
                        xtype: 'extensible.calendarlist',
                        store: this.calendarStore,
                        border: false,
                        width: 178
                    	},*/
                    	{
                        //任务列表
                        xtype: 'extensible.tasklist',
                        store: this.taskStore,
                        border: false,
                        width: 178,
                        scroll: 'vertical'
                    }
        			]
        			//返回到Timesheet_users
//                    buttons: [{
//                    			text: '返回',
//                    			id :'return-button',
//                    			itemId: 'return-button',
//                    			handler: function(){
//                    				
//                    				timesheetWindowClose(Ext.get("user-id").dom.innerHTML, Ext.get("date").dom.innerHTML, Ext.get("pre_status").dom.innerHTML);
//                    				
//                    				Ext.MessageBox.confirm('提交任务', '是否要提交当天任务(提交之后可以继续修改直到审核通过)?', callback);
//                    				function callback(id)
//                    				{
//                    					console.log('Ext.MessageBox.confirm   :' + id);
//                    					if(id == 'yes')
//                    					{
//                    						//提交审核当天的events
//		                    				var requestConfig = {
//		                    					url: '/confirm_actual_tasks',
//		                    					callback: function(options, success, response){
//		                    						console.log('your events has been Confirmed');
//		                    						//提交完成后刷新页面
//		                    						location.reload();
//		                    					}
//		                    				}
//		                    				Ext.Ajax.request(requestConfig);
//                    					}
//                    				}
//                    				
//                    			}
//                    			//hidden: false
//                    		 }]
                },{
                    xtype: 'extensible.calendarpanel',
                    eventStore: this.eventStore,
                    calendarStore: this.calendarStore,
                    border: false,
                    id:'app-calendar',
                    region: 'center',
                    activeItem: 1, // 设置初始显示的Tab	0 day 1 week
                    dailyStore: this.dailyStore,
                    
                    // Any generic view options that should be applied to all sub views:
                    viewConfig: {
                        //enableFx: false,
                        //ddIncrement: 10, //only applies to DayView and subclasses, but convenient to put it here
                        //viewStartHour: 6,
                        //viewEndHour: 18,
                        //minEventDisplayMinutes: 15
                        showTime: false
                    },
                    
                    // View options specific to a certain view (if the same options exist in viewConfig
                    // they will be overridden by the view-specific config):
                    monthViewCfg: {
                        showHeader: true,
                        showWeekLinks: true,
                        showWeekNumbers: true
                    },
                    
                    multiWeekViewCfg: {
                        //weekCount: 3
                    },
                    
                    // Some optional CalendarPanel configs to experiment with:
                    //readOnly: true,
                    //showDayView: false,
                    //showMultiDayView: true,
                    //showWeekView: false,
                    //showMultiWeekView: false,
                    showMonthView: false,
                    //showNavBar: false,
                    //showTodayText: false,
                    //showTime: false,
                    //editModal: true,
                    //enableEditDetails: false,
                    //title: 'My Calendar', // the header of the calendar, could be a subtitle for the app
                    
                    listeners: {
                        'eventclick': {
                            fn: function(vw, rec, el){
                                this.clearMsg();
                            },
                            scope: this
                        },
                        'eventover': function(vw, rec, el){
                            //console.log('Entered evt rec='+rec.data[Extensible.calendar.data.EventMappings.Title.name]', view='+ vw.id +', el='+el.id);
                        },
                        'eventout': function(vw, rec, el){
                            //console.log('Leaving evt rec='+rec.data[Extensible.calendar.data.EventMappings.Title.name]+', view='+ vw.id +', el='+el.id);
                        },
                        'eventadd': {
                            fn: function(cp, rec){
                                this.showMsg('Event '+ rec.data[Extensible.calendar.data.EventMappings.Title.name] +' was added');
                                //console.log('event add function called');
                              
                            },
                            scope: this
                        },
                        'eventupdate': {
                            fn: function(cp, rec){
                                this.showMsg('Event '+ rec.data[Extensible.calendar.data.EventMappings.Title.name] +' was updated'); 
                            },
                            scope: this
                        },
                        'eventdelete': {
                            fn: function(cp, rec){
                                this.showMsg('Event '+ rec.data[Extensible.calendar.data.EventMappings.Title.name] +' was deleted');
                            },
                            scope: this
                        },
                        'eventcancel': {
                            fn: function(cp, rec){
                                // edit canceled
                            },
                            scope: this
                        },
                        'viewchange': {
                            fn: function(p, vw, dateInfo){
                                if(dateInfo){
                                    this.updateTitle(dateInfo.viewStart, dateInfo.viewEnd);
                                }
                            },
                            scope: this
                        },
                        'dayclick': {
                            fn: function(vw, dt, ad, el){
                                this.clearMsg();
                            },
                            scope: this
                        },
                        'rangeselect': {
                            fn: function(vw, dates, onComplete){
                                this.clearMsg();
                            },
                            scope: this
                        },
                        'eventmove': {
                            fn: function(vw, rec){
                                var mappings = Extensible.calendar.data.EventMappings,
                                    time = rec.data[mappings.IsAllDay.name] ? '' : ' \\a\\t g:i a';
                                
                                rec.commit();
                                
                                this.showMsg('Event '+ rec.data[mappings.Title.name] +' was moved to '+
                                    Ext.Date.format(rec.data[mappings.StartDate.name], ('F jS'+time)));
                            },
                            scope: this
                        },
                        'eventresize': {
                            fn: function(vw, rec){
                                rec.commit();
                                this.showMsg('Event '+ rec.data[Extensible.calendar.data.EventMappings.Title.name] +' was updated');
                            },
                            scope: this
                        },
                        'eventdelete': {
                            fn: function(win, rec){
                                this.eventStore.remove(rec);
                                this.showMsg('Event '+ rec.data[Extensible.calendar.data.EventMappings.Title.name] +' was deleted');
                            },
                            scope: this
                        },
                        'initdrag': {
                            fn: function(vw){
                                // do something when drag starts
                            },
                            scope: this
                        }
                    }
                }]
            }]
        });
        
        //窗口关闭事件
        
        //审核显示编辑按钮
//        console.log('mode      ' + Ext.get("mode").dom.innerHTML);
//        if (Ext.get("mode").dom.innerHTML == 'edit')
//        {
//        	//console.log('审核显示编辑按钮');
//        	var editBtn = Ext.getCmp('return-button');
//        	editBtn.hide();
//        }
        
//        var requestConfig = {
//			url: '/get_actual_daily_status',
//			method: 'get',
//			callback: function(options, success, response){
//				var json = eval("(" + response.responseText + ")");
//				console.log(json.result);
//				//如果已提交，则禁用提交按钮
//				if(json.result == true)
//				{
//					var appWest = Ext.getCmp('confirm-button');
//        			appWest.disable();    			
//        			//appWest.hide();
//            		
//        			appCalendar = Ext.getCmp('app-calendar');
//        			console.log(appCalendar);
//        			appCalendar.showDayView = false;
//        			//appCalendar.disable();
//        			        			
//				}
//			}
//		}
//		Ext.Ajax.request(requestConfig);
                    				
        
        //console.log(appWest);
    },
    
    // The CalendarPanel itself supports the standard Panel title config, but that title
    // only spans the calendar views.  For a title that spans the entire width of the app
    // we added a title to the layout's outer center region that is app-specific. This code
    // updates that outer title based on the currently-selected view range anytime the view changes.
    updateTitle: function(startDt, endDt){
        var p = Ext.getCmp('app-center'),
            fmt = Ext.Date.format;
        
        if(Ext.Date.clearTime(startDt).getTime() == Ext.Date.clearTime(endDt).getTime()){
            p.setTitle(fmt(startDt, 'F j, Y'));
        }
        else if(startDt.getFullYear() == endDt.getFullYear()){
            if(startDt.getMonth() == endDt.getMonth()){
                p.setTitle(fmt(startDt, 'F j') + ' - ' + fmt(endDt, 'j, Y'));
            }
            else{
                p.setTitle(fmt(startDt, 'F j') + ' - ' + fmt(endDt, 'F j, Y'));
            }
        }
        else{
            p.setTitle(fmt(startDt, 'F j, Y') + ' - ' + fmt(endDt, 'F j, Y'));
        }
    },
    
    // This is an application-specific way to communicate CalendarPanel event messages back to the user.
    // This could be replaced with a function to do "toast" style messages, growl messages, etc. This will
    // vary based on application requirements, which is why it's not baked into the CalendarPanel.
    showMsg: function(msg){
        Ext.fly('app-msg').update(msg).removeCls('x-hidden');
    },
    
    clearMsg: function(){
        Ext.fly('app-msg').update('').addCls('x-hidden');
    }
});

Ext.onReady(function() {
    Ext.create('Extensible.App');
});

$(window).unload(function(){
       //离开页面时执行
       if(Ext.get("mode").dom.innerHTML == 'viewedit')
       {
       		console.log("viewedit mode");
       		timesheetWindowClose(Ext.get("user-id").dom.innerHTML, Ext.get("date").dom.innerHTML, Ext.get("pre_status").dom.innerHTML);
       }       
});
