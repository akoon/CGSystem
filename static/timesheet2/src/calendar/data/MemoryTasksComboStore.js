Ext.define('Extensible.calendar.data.MemoryTasksComboStore', {
    extend: 'Ext.data.Store',
    model: 'Extensible.calendar.data.TaskModel',
	autoLoad: true,
	autoSync : true,
	buffered : true,
	remoteFilter : true,
	proxy: {
		type: 'ajax',
		api: {
				read: '/get_user_tasks_combo/' + Ext.get("user-id").dom.innerHTML
		},
		reader: {
				type: 'json',
				root: 'tasks',
				successProperty: 'success'
		}
	}
});
