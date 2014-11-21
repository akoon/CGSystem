Ext.define('Extensible.calendar.data.MemoryUserComboStore', {
    extend: 'Ext.data.Store',
    model: 'Extensible.calendar.data.UserModel',
	autoLoad: true,
	
	proxy: {
		type: 'ajax',
		api: {
				read: '/CalendarSys/get_user_combo'
		},
		reader: {
				type: 'json'
		}
	}
});
