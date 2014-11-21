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
Ext.define('Ext.calendar.form.field.MissionCombo', {
    extend: 'Ext.form.field.MissionCombo',
    alias: 'widget.missioncombo',

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

        this.callParent();
    }
});
