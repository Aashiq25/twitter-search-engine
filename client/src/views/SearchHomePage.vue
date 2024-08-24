<template>
    <div class="tw-body">
        <div class="flex flex-row justify-center items-center">
            <InlineSvg
                src="app-icon"
                iconClass="icon size-120 mr-5"
            ></InlineSvg>
            <div class="title-text">Lambda</div>
        </div>
        <div class="flex flex-row mt-10 w-96">
            <el-input
                @keyup.native.enter="routeToSearchResults"
                v-model="searchQuery"
                class="w-full tw-search-bar mr-2"
                clearable
                placeholder="Search here"
            >
            </el-input>

            <el-button
                @click="routeToSearchResults"
                icon="search"
                class="tw-search-button"
                >Search</el-button
            >
        </div>
    </div>
</template>
<script>
export default {
    data: () => ({
        searchQuery: '',
    }),
    methods: {
        routeToSearchResults() {
            if (!this.$_.isEmpty(this.searchQuery)) {
                this.$router.push({
                    path: 'searchresults',
                    query: { searchquery: this.searchQuery },
                })
            }
        },
    },
}
</script>
