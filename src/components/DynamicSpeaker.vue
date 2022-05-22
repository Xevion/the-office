<template>
    <span>
        <template v-for="(constituent, index) in texts">
            <router-link class="speaker-link" v-if="constituent.route" :key="index" :to="constituent.route">
                {{ constituent.text }}
            </router-link>
            <span class="speaker-bg" v-else :key="index">{{ constituent }}</span>
        </template>
    </span>
</template>

<script>
export default {
    name: "DynamicSpeaker",
    props: {
        text: {type: String, required: true},
        characters: {type: Object, required: true}
    },
    computed: {
        texts() {
            return this.text.split(/({[^}]+})/).map((item) => {
                const id = item.substring(1, item.length - 1)
                if (item.startsWith('{'))
                    return {
                        text: this.characters[id],
                        route: {
                            name: 'Character', params: {character: id}
                        }
                    }
                else
                    return item;
            });
        }
    }
}
</script>

<style scoped>

</style>
