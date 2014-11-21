Ext.ns('App');

//Ext.Loader.setConfig({enabled: true, disableCaching : false });
//Ext.Loader.setPath('Sch', '../../../ExtScheduler2.x/js/Sch');
//Ext.Loader.setPath('Gnt', '../../js/Gnt');

Ext.require([
    'Gnt.panel.Gantt',
    'Gnt.column.PercentDone',
    'Gnt.column.StartDate',
    'Gnt.column.EndDate',
    'Sch.plugin.TreeCellEditing'
]);

//隐藏除当前节点外的所有兄弟节点
//function clearNodes(node)
//{
//	// 得到当前节点父节点下所有子节点（也就是当前节点的同级节点）
//	var nodes = node.parentNode.childNodes;
//	
//	// 隐藏除当前节点之外其他节点的子节点
//    for(var i = 0; i < nodes.length; i++) {
//        if(nodes[i] != node) {
//        	nodes[i].collapse();
//            nodes[i].clear();
//            
//        }
//    }
//    
//    return node.parentNode;
//}

Ext.onReady(function() { Localize(); App.Gantt.init(); 

	//项目选择
//	Ext.regModel('ProjModel', {
//	    fields: [{name: 'name'},{name: 'id'}]
//	});
//	
//	var projStore = Ext.create('Ext.data.Store',{
//		model : 'ProjModel',
//		autoLoad: true,
//		proxy: {
//	        type: 'ajax',
//	        api: {
//				read: '/gantt_projlist'
//			},
//			reader: {
//				type: 'json',
//				root: 'tasks',
//				successProperty: 'success'
//			}
//	    }
//	});
	
	Ext.create('Ext.form.Panel',{
//		title:'项目选择',
		renderTo: Ext.get('gnt_projs'),
		bodyPadding: 0,
		frame : true,
		height:32,
		width:'100%',
		defaults:{//统一设置表单字段默认属性
			labelSeparator :'：',//分隔符
			labelWidth : 40,//标签宽度
			width : 200,//字段宽度
			labelAlign : 'left'//标签对齐方式
		},
		items:[{
			xtype : 'combo',
			listConfig : {
				emptyText : '未找到匹配值'
				//maxHeight : 60//设置下拉列表的最大高度为60像素
			},
			name:'post',
			autoSelect : true,
			fieldLabel:'项目',
			triggerAction: 'all',//单击触发按钮显示全部数据
			store : projStore,//设置数据源
			displayField:'name',//定义要显示的字段
			valueField:'id',//定义值字段
			queryMode: 'remote',
			forceSelection : true,//要求输入值必须在列表中存在
			typeAhead : true,//允许自动选择匹配的剩余部分文本
			editable : false,
			value: 0,
			listeners:{
				"select":function(){
					//页面跳转
					window.location.href='/ProjectManSys/gantt/?proj=' + this.getValue();
				}
			}
		}]
	});
});

App.Gantt = {

    // Initialize application
    init: function (serverCfg) {
        Ext.QuickTips.init();
        
        var proj = Ext.get('proj').dom.innerHTML;
        var startdate = Ext.get('startdate').dom.innerHTML.split('-');
        var endate = Ext.get('endate').dom.innerHTML.split('-');
        
        console.log('startdate  ' + startdate);
        console.log('endate     ' + endate);
        
        if(proj == '' || proj == null)
        {
        	proj = 0;
        }

        var taskStore = Ext.create("Gnt.data.TaskStore", {
            model : 'Gnt.model.Task',
            autoLoad: true,
            autoSync: true,
            proxy : {
                type : 'ajax',
                method: 'GET',
                api: {
                    read: '/get_gantt_tasks/?proj=' + proj
                    //update: '/get_g',
                    
                },
                reader: {
                    type : 'json',
                    // records will have a 'Task' tag
                    record: "Task",
                    root: "Tasks",
                    idProperty: "Id"
                    
                }
            }
        });
		
        var dependencyStore = Ext.create("Ext.data.Store", {
            autoLoad: true,
            model : 'Gnt.model.Dependency',
            proxy: {
                type : 'ajax',
                url: '/static/extraneous/gantt/dependencies.xml',
                method: 'GET',
                reader: {
                    type : 'xml',
                    root : 'Links',
                    record: 'Link' // records will have a 'Link' tag
                }
            }
        });

        var colSlider = Ext.create("Ext.slider.Single", {
            width: 120,
            value: 100, // TODO Sch.PresetManager.getPreset('weekAndDayLetter').timeColumnWidth,
            minValue: 80,
            maxValue: 240,
            increment: 10
        });
		
		/*
        var cellEditing = Ext.create('Sch.plugin.TreeCellEditing', {
            clicksToEdit: 1,
            listeners : {
                beforeedit : 
                	function() { 
                		//return !Ext.getCmp('demo-readonlybutton').pressed; 
                	}
            }
        });
		*/
		
		var _h = $(window).height();
        var _w = $(window).width();
		
        //当前日期
        var currentDate = new Date();
        console.log(currentDate.getDate());
        
        var g = Ext.create('Gnt.panel.Gantt', {
            height: _h,
            width: '100%',
            renderTo: Ext.get('gnt_table'),
            leftLabelField: 'Name',
            highlightWeekends: true,
            loadMask: true,
            enableProgressBarResize: true,
            enableDependencyDragDrop: true,
            //snapToIncrement : true,
            startDate: new Date(parseInt(startdate[0]), parseInt(startdate[1]) - 1, parseInt(startdate[2])),//new Date(currentDate.getFullYear(), currentDate.getMonth() - 6, 1),	//开始日期
            endDate: new Date(parseInt(endate[0]), parseInt(endate[1]), parseInt(endate[2])),//Sch.util.Date.add(new Date(currentDate.getFullYear(), currentDate.getMonth() + 6, 1), Sch.util.Date.WEEK, 10),	//结束日期
            viewPreset: 'dayAndMonth',
			cascadeChanges: true,
			id:		'ganttPanel',
			itemId:	'ganttPanel',
			stripeRows: true,
			
            eventRenderer: function (taskRecord) {
                return {
                    ctcls : taskRecord.get('Id') // Add a CSS class to the task element
                };
            },

            tooltipTpl: new Ext.XTemplate(
                '<ul class="taskTip">',
                    '<li><strong>Task:</strong>{Name}</li>',
                    '<li><strong>Start:</strong>{[Ext.Date.format(values.StartDate, "y-m-d")]}</li>',
                    '<li><strong>Duration:</strong> {Duration}d</li>',
                    '<li><strong>Progress:</strong>{PercentDone}%</li>',
                '</ul>'
            ).compile(),


            // Setup your static columns
            columns: [
                {
                    xtype : 'treecolumn',
                    itemId: 'treecolumnObj',
                    header: 'Tasks',
                    sortable: true,
                    dataIndex: 'Name',
                    width: 200,
                    field: {
                        allowBlank: false
                    }
                },
                Ext.create('Gnt.column.StartDate'),
                Ext.create('Gnt.column.EndDate'),
                Ext.create('Gnt.column.PercentDone'),
                Ext.create('Gnt.column.Status'),
                Ext.create('Gnt.column.Assign'),
                Ext.create('Gnt.column.Remark'),
                Ext.create('Gnt.column.Feedback')
                
            ],
			
            taskStore: taskStore
            //dependencyStore: dependencyStore
            //plugins: [cellEditing]
//            tbar: [{
//					text:'显示当前项目',
//					id :'expandSelected',
//        			itemId: 'expandSelected',
//        			handler: function(){
//        				var mdl = g.getSelectionModel().getSelection();
//                    	if(mdl.length != 0)
//                    	{
//                    		node = mdl[0];
//                    		console.log(node);
//                    		console.log(node.parentNode);
//    						do
//    						{
//    							node = clearNodes(node);
//    						}
//    						while (node.getDepth() != 0)
//						    g.refreshView();
//                    	}
//        			}
//        		}]
        });
        
        //设置只读
        //g.setReadOnly(true);
		console.log(g);
        colSlider.on({
            change: function (s, v) {
                g.setTimeColumnWidth(v, true);
            },
            changecomplete: function (s, v) {
                g.setTimeColumnWidth(v);
            }
        });
    }
};
