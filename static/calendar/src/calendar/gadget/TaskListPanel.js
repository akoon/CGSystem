Ext.define('Extensible.calendar.gadget.TaskListPanel' ,{
    extend: 'Ext.grid.Panel',
    alias: 'widget.extensible.tasklist',

    title: 'Task List',
	layout: 'fit',
    autoShow: true,
	
	requires: [
        'Ext.XTemplate'
    ],
    
    initComponent: function() {

        this.columns = [
            {header: 'name',  dataIndex: 'name',  flex: 1}
        ];
        
        //this.store = this.taskStore;
        
        this.callParent(arguments);
    }
});
