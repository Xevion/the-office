<template>
    <div id="app">
        <b-container :fluid=true class="py-5 px-5">
            <b-row>
                <b-col lg="3" xl="2" md="12">
                    <SeasonList></SeasonList>
                </b-col>
                <b-col>
                    <router-view/>
                </b-col>
                <b-col md="0" lg="1" xl="2">

                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<style>
    body { background-color: #0a0a0a; }
</style>

<script>
import SeasonList from './components/SeasonList.vue';

export default {
  name: 'App',
  components: {
    SeasonList,
  },
};
</script>
