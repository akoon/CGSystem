/**
 * @class Ext.calendar.data.EventMappings
 * @extends Object
 * A simple object that provides the field definitions for Event records so that they can be easily overridden.
 */
Ext.ns('Ext.calendar.data');

Ext.calendar.data.EventMappings = {
	/*
	EventId: {
        name: 'EventId',
        mapping: 'id',
        type: 'int'
    },
    Title: {
        name: 'Title',
        mapping: 'title',
        type: 'string'
    },
    StartDate: {
        name: 'StartDate',
        mapping: 'start',
        type: 'date',
        dateFormat: 'c'
    },
    EndDate: {
        name: 'EndDate',
        mapping: 'end',
        type: 'date',
        dateFormat: 'c'
    },
    Notes: {
        name: 'Notes',
        mapping: 'notes',
        type: 'string'
    }*/
	
    EventId: {
        name: 'EventId',
        mapping: 'id',
        type: 'int'
    },
    CalendarId: {
        name: 'CalendarId',
        mapping: 'cid',
        type: 'int'
    },
    Title: {
        name: 'Title',
        mapping: 'title',
        type: 'string'
    },
    Task: {
        name: 'Task',
        mapping: 'task',
        type: 'int'
    },
    StartDate: {
        name: 'StartDate',
        mapping: 'start',
        type: 'date',
        dateFormat: 'time'
    },
    EndDate: {
        name: 'EndDate',
        mapping: 'end',
        type: 'date',
        dateFormat: 'time'
    },
    Notes: {
        name: 'Notes',
        mapping: 'notes',
        type: 'string'
    },
    IsAllDay: {
        name: 'IsAllDay',
        mapping: 'ad',
        type: 'boolean'
    },
    Reminder: {
        name: 'Reminder',
        mapping: 'rem',
        type: 'string'
    },
    IsNew: {
        name: 'IsNew',
        mapping: 'n',
        type: 'boolean'
    }
    
};
