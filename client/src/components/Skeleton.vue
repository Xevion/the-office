<template>
    <div class="skeleton"></div>
</template>
<style lang="scss" scoped>
.skeleton {
    background-color: $grey-4;
    background-image: linear-gradient(90deg, $grey-4, $grey-6, $grey-4);
    animation: 1.5s ease-in-out 0s infinite normal none running SkeletonLoading;
    width: 100%;
    display: block;
    line-height: 1;
    background-size: 200px 100%;
    background-repeat: no-repeat;
    border-radius: 3px;
}

@-webkit-keyframes SkeletonLoading {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

@keyframes SkeletonLoading {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

span {
    font-size: 24px;
}
</style>
