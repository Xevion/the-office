<template>
    <div>
        <b-card>
            <h4>{{ this.$route.params.character }}</h4>
        </b-card>
    </div>
</template>

<style lang="scss" scoped>
.card-body h4 {
    text-transform: capitalize;
}
</style>

<script>
export default {
};
</script>
