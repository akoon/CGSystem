Ext.define('Extensible.calendar.view.TaskList' ,{
    extend: 'Ext.grid.Panel',
    alias: 'widget.tasklist',

    title: 'Task List',
	layout: 'fit',
    autoShow: true,
	
    initComponent: function() {

        this.columns = [
            {header: 'name',  dataIndex: 'name',  flex: 1}
        ];
        
        this.store = this.tasklistStore;
        
        this.callParent(arguments);
    }
});
