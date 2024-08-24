<template>
    <div class="tw-header flex flex-row justify-between pl-10 pr-5">
        <div class="flex flex-row">
            <div
                @click="changeTab('search')"
                :class="[
                    'tw-tabs flex flex-col h-full',
                    activeTab == 'search' && 'active',
                ]"
            >
                <div class="flex flex-row items-center justify-between h-full">
                    <InlineSvg
                        src="magnifier"
                        iconClass="icon size-sm"
                    ></InlineSvg>
                    <div class="ml-2">Search</div>
                </div>
                <div v-if="activeTab == 'search'" class="tab-border"></div>
            </div>

            <div
                @click="changeTab('analytics')"
                :class="[
                    'tw-tabs ml-10 flex flex-col h-full',
                    activeTab == 'analytics' && 'active',
                ]"
            >
                <div class="flex flex-row items-center justify-between h-full">
                    <InlineSvg
                        src="analytics"
                        iconClass="icon size-sm"
                    ></InlineSvg>
                    <div class="ml-2">Dashboard</div>
                </div>
                <div v-if="activeTab == 'analytics'" class="tab-border"></div>
            </div>
            <div></div>
        </div>
        <div>
            <div class="flex flex-row justify-center items-center">
                <InlineSvg src="app-icon" iconClass="icon size-l"></InlineSvg>
                <div class="title-text font-color1 size-18 ml-2">Lambda</div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'Header',
    data: () => ({
        activeTab: 'search',
    }),
    created() {
        if (this.$route.name == 'Analytics') {
            this.activeTab = 'analytics'
        }
    },
    methods: {
        changeTab(name) {
            this.activeTab = name
            if (name == 'analytics') {
                this.$router.push({ path: 'analytics' })
            } else if (name == 'search') {
                this.$router.push({ path: 'search' })
            }
        },
    },
}
</script>
