<template>
    <div id="app">
        <router-view/>
        <b-container fluid=true class="py-5 px-5">
            <b-row>
                <b-col lg="3" xl="2" md="12">
                    <SeasonList></SeasonList>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import SeasonList from './components/SeasonList.vue';

export default {
  name: 'App',
  components: {
    SeasonList,
  },
};
</script>
