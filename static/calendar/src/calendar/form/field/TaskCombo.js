/**
 * @class Ext.calendar.form.field.ReminderCombo
 * @extends Ext.form.ComboBox
 * <p> 任务列表 combobox </p>
 * <p>A custom combo used for choosing a reminder setting for an event.</p>
 * <p>This is pretty much a standard combo that is simply pre-configured for the options needed by the
 * calendar components. The default configs are as follows:<pre><code>
    width: 200,
    fieldLabel: 'Reminder',
    queryMode: 'local',
    triggerAction: 'all',
    forceSelection: true,
    displayField: 'desc',
    valueField: 'value'
</code></pre>
 * @constructor
 * @param {Object} config The config object
 */
Ext.define('Extensible.calendar.form.field.TaskCombo', {
    extend: 'Ext.form.ComboBox',
    alias: 'widget.extensible.taskcombo',

    fieldLabel: 'Task',
    queryMode: 'local',
    triggerAction: 'all',
    forceSelection: true,
    displayField: 'name',
    valueField: 'id',
    emptyText: "选择任务",
	selectedItem : 0,
    // private
    initComponent: function() {
    	//this.store = this.tasklistStore;
        
    	/*
        this.store = this.store || new Ext.data.ArrayStore({
            fields: ['value', 'desc'],
            idIndex: 0,
            data: [
            	['1', 'sh18_layout'],
            	['2', 'sh17_comp'],
            	['3', 'sh17_fx'],
            	['4', 'sh17_lighting'],
            	['5', 'sh17_rending'],
            	['6', 'sh17_animation'],
            	['7', '王飞鹏：因身体不适请假三天（2012年12月7日、2012年12月10日、2012年12月11日）'],
            	['8', '信息技术部会议'],
            	['10', '加班']
            	
           ]
        });
        */
        var store = Ext.create('Ext.data.Store', { 
		      model: 'Ext.calendar.data.TaskModel', 
		      proxy: { 
		          type: 'ajax', 
		          url: '/get_user_tasks_combo' 
		      }, 
		      autoLoad: true, 
		      remoteSort:true 
		  }); 
  		this.store = store;
        console.log("store    :" + this.store);
        
        this.valueField = Ext.calendar.data.EventMappings.Task.name;
        //this.displayField = Ext.calendar.data.EventMappings.Title.name;
        
        this.callParent();
    },

        // inherited docs
    setValue: function(value) {
    	console.log("setValue function called");
        
        
        console.log("this.getValue();   " + this.getValue());
        
        this.selectedItem = this.getValue();
        
        console.log("this.selectedItem   " + this.selectedItem);
        
        this.callParent(arguments);
    }
});
