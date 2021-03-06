<template>

  <div>
    <div v-if="showRecentOnly" ref="recentHeader">
      <h1>{{ $tr('recentTitle') }}</h1>
      <report-subheading />
    </div>

    <report-table v-if="standardDataTable.length" :caption="$tr('channelList')">
      <thead slot="thead">
        <tr>
          <header-cell
            :text="$tr('channels')"
            align="left"
            :sortable="true"
            :column="tableColumns.NAME"/>
          <header-cell
            :text="$tr('lastActivity')"
            align="left"
            :sortable="true"
            :column="tableColumns.DATE"/>
        </tr>
      </thead>
      <tbody slot="tbody">
        <template v-for="channel in standardDataTable">
          <tr :key="channel.id">
            <name-cell :kind="CHANNEL" :title="channel.title" :link="reportLink(channel.id)"/>
            <activity-cell :date="channel.lastActive"/>
          </tr>
        </template>
      </tbody>
    </report-table>
  </div>

</template>


<script>

  const { ContentNodeKinds } = require('kolibri.coreVue.vuex.constants');
  const { PageNames } = require('../../constants');
  const reportConstants = require('../../reportConstants');
  const reportGetters = require('../../state/getters/reports');

  module.exports = {
    name: 'channelList',
    $trNameSpace: 'coachRecentPageChannelList',
    $trs: {
      recentTitle: 'Recent Activity',
      channels: 'Channels',
      channelList: 'Channel list',
      lastActivity: 'Last active',
    },
    components: {
      'report-table': require('./report-table'),
      'report-subheading': require('./report-subheading'),
      'header-cell': require('./table-cells/header-cell'),
      'name-cell': require('./table-cells/name-cell'),
      'activity-cell': require('./table-cells/activity-cell'),
    },
    computed: {
      CHANNEL() {
        return ContentNodeKinds.CHANNEL;
      },
      tableColumns() {
        return reportConstants.TableColumns;
      },
    },
    methods: {
      reportLink(channelId) {
        const linkTargets = {
          [PageNames.RECENT_CHANNELS]: PageNames.RECENT_ITEMS_FOR_CHANNEL,
          [PageNames.TOPIC_CHANNELS]: PageNames.TOPIC_CHANNEL_ROOT,
          [PageNames.LEARNER_CHANNELS]: PageNames.LEARNER_CHANNEL_ROOT,
        };
        return {
          name: linkTargets[this.pageName],
          params: {
            classId: this.classId,
            channelId,
          },
        };
      },
    },
    vuex: {
      getters: {
        channels: state => state.core.channels.list,
        standardDataTable: reportGetters.standardDataTable,
        classId: state => state.classId,
        pageName: state => state.pageName,
        showRecentOnly: state => state.pageState.showRecentOnly,
      },
    },
  };

</script>


<style lang="stylus" scoped></style>
