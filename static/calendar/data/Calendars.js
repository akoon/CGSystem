/*!
 * Extensible 1.5.1
 * Copyright(c) 2010-2011 Extensible, LLC
 * licensing@ext.ensible.com
 * http://ext.ensible.com
 */
Ext.define('Extensible.calendar.data.Calendars', {
    constructor: function() {
        return {
            "calendars" : [{
                "id"    : 1,
                "title" : "Editing",
                "color" : 2
            },{
                "id"    : 2,
                "title" : "Confirmed",
                "color" : 22
            },{
                "id"    : 3,
                "title" : "Passed",
                "color" : 7
            },{
                "id"    : 4,
                "title" : "Returned",
                //"hidden" : true, // optionally init this calendar as hidden by default
                "color" : 26
            },
            {
                "id"    : 5,
                "title" : "Freeze",
                //"hidden" : true, // optionally init this calendar as hidden by default
                "color" : 27
            }]
        };
    }
});
