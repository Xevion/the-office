<template>
    <div>
        <b-breadcrumb :items="breadcrumbs" />
        <b-card>
            <h3>What is this?</h3>
            <p>
                This app is a quote viewing and searching app centered around the hit workplace comedy
                and sitcom 'The Office'. I made it in order to learn Vue, API creation and a variety of
                techniques and frameworks. Since inception, it's evolved and improved from something simple to
                a passion project where I have poured a great deal of work into.
            </p>
            <h3>How does it work?</h3>
            <p>
                Most of the UI is self-explanatory and designed to be easy to use.
            </p>
            <ul>
                <li>
                    You can select episodes with the drop-down based selector on the left.
                </li>
                <li>
                    You can search for quotes with the search bar at the top left.
                </li>
                <li>
                    You can browse characters by clicking the 'Characters' link at the top or by finding
                    and clicking on individual characters inside the episodes themselves.
                </li>
            </ul>
            <h3>I found an error in the quotes, how can I help fix it?</h3>
            <p>
                Currently, this part of the application is rather difficult to explain the workings of.
                There will be a system in place to explain how errors can be amended and taken care of,
                but that will be explained and added later once I have time.
                For now, please open a new issue on <a href="https://github.com/Xevion/the-office/issues/new">the github</a>.
            </p>
        </b-card>
    </div>
</template>

<script>
export default {
    name: "About",
    computed: {
        breadcrumbs() {
            return [
                {text: 'Home', to: {name: 'Home'}},
                {text: 'About', active: true}
            ]
        }
    }
}
</script>

<style scoped>

</style>
