Ext.define('Extensible.calendar.data.MemoryMissionsComboStore', {
    extend: 'Ext.data.Store',
    model: 'Extensible.calendar.data.TaskModel',
	autoLoad: true,
	
	proxy: {
		type: 'ajax',
		api: {
				read: '/get_user_missions_combo',
		},
		reader: {
				type: 'json',
				root: 'tasks',
				successProperty: 'success'
		}
	}
});
