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
Ext.define('Ext.calendar.form.field.MissionsCombo', {
    extend: 'Ext.form.field.ComboBox',
    alias: 'widget.missionscombo',

    fieldLabel: 'Mission',
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
        
        var store = Ext.create('Ext.data.Store', { 
		      model: 'Ext.calendar.data.TaskModel', 
		      proxy: { 
		          type: 'ajax', 
		          url: '/get_user_missions_combo' 
		      }, 
		      autoLoad: true, 
		      remoteSort:true 
		  }); 
  		this.store = store;
        console.log("store    :" + this.store);
        this.callParent();
    }
});
