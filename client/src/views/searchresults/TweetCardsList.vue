<template>
    <div v-if="loading" class="p-5 overflow-y-scroll">
        <el-skeleton :rows="4" animated />
        <el-skeleton :rows="4" animated class="mt-10" />
        <el-skeleton :rows="4" animated class="mt-10" />
    </div>
    <el-tabs v-else v-model="currentTab" class="pl-3 pr-3">
        <el-tab-pane
            label="Tweet Results"
            name="tweet"
            class="overflow-y-scroll tab-height1"
        >
            <div
                v-if="totalDocs && timeTaken"
                class="mt-3 flex items-center justify-center fetched-tweet-text"
            >
                {{ `Fetched ${totalDocs} tweets in ${timeTaken}` }}
            </div>
            <div class="flex flex-col p-5">
                <TweetCard
                    v-for="(tweet, index) in tweetsList"
                    :key="`tw-card-${index}`"
                    :class="['results-card', index != 0 && 'mt-4']"
                    :tweet="tweet"
                ></TweetCard>

                <div class="flex justify-center w-full mt-5">
                    <el-pagination
                        background
                        @current-change="nextPage"
                        :current-page.sync="pageNo"
                        :page-size="20"
                        layout="prev, pager, next"
                        :total="totalDocs"
                    >
                    </el-pagination>
                </div></div
        ></el-tab-pane>
        <el-tab-pane
            label="Analytics"
            name="analytics"
            class="bg-grey tab-height2 rounded-xl"
        >
            <QueryAnalytics :chartData="chartData"></QueryAnalytics>
        </el-tab-pane>
    </el-tabs>
</template>
<script>
import {
    filterFields,
    arrayFields,
    sentimentVsLabel,
} from '@/helpers/constants'
import QueryAnalytics from './QueryAnalytics.vue'
import TweetCard from './TweetCard.vue'
export default {
    components: {
        QueryAnalytics,
        TweetCard,
    },
    data: () => ({
        tweetsList: [],
        loading: true,
        pageNo: 1,
        totalDocs: null,
        chartData: [],
        currentTab: 'tweet',
        timeTaken: null,
        sentimentVsLabel,
    }),
    created() {
        this.fetchResults()
    },
    computed: {
        routeQueries() {
            return this.$route.query || {}
        },
    },
    watch: {
        routeQueries() {
            this.pageNo = 1
            this.fetchResults()
        },
    },
    methods: {
        async fetchResults() {
            let { queryParams } = this.constructQueries()
            this.loading = true
            try {
                let response = await this.$axios.post(`api/search`, queryParams)
                this.tweetsList = response?.data?.response?.docs || []
                let allHighlights = response?.data?.highlighting
                this.tweetsList.forEach((tweet) => {
                    let highlightedText =
                        this.$_.get(allHighlights, [
                            `${tweet.id}`,
                            'tweet_text',
                            '0',
                        ]) || tweet.tweet_text

                    let urls_regex = /((https?:\/\/\S+))/g
                    let replaceUrls = '<a target="_blank" href="$1">$1</a>'
                    highlightedText = highlightedText.replace(
                        urls_regex,
                        replaceUrls
                    )

                    let mentions_regex = /(^|[^@\w])@(\w{1,15})\b/g
                    let replace =
                        '<span style="color: rgb(29, 155, 240);">$1<a target="_blank" href="http://twitter.com/$2">@$2</a></span>'

                    highlightedText = highlightedText.replace(
                        mentions_regex,
                        replace
                    )

                    let hashtags_regex =
                        /(^|[^#\w])#(\w{1,100}|<em>\w{1,100}<\/em>)/g
                    let replaceHashTags =
                        '<span style="color: rgb(29, 155, 240);">$1<a target="_blank" href="http://localhost:8080/searchresults?searchquery=$2">#$2</a></span>'

                    highlightedText = highlightedText.replace(
                        hashtags_regex,
                        replaceHashTags
                    )

                    this.$set(tweet, 'highlightedText', highlightedText)
                })
                this.totalDocs = response?.data?.response?.numFound || 0
                this.timeTaken = response?.data?.time_taken
                this.chartData = response?.data?.facets
                this.loading = false
            } catch (error) {
                this.$message.error(error?.message || 'Server Error')
            }
        },
        nextPage() {
            this.fetchResults()
        },
        constructQueries() {
            let params = {}
            params.query = this.routeQueries.searchquery
            params.pageNo = this.pageNo
            params.pageSize = 20
            filterFields.forEach((field) => {
                if (!this.$_.isEmpty(this.routeQueries[field])) {
                    if (arrayFields.includes(field)) {
                        this.$set(
                            params,
                            `${field}`,
                            JSON.parse(
                                decodeURIComponent(this.$route.query[field])
                            )
                        )
                    } else {
                        this.$set(
                            params,
                            field,
                            decodeURIComponent(this.$route.query[field])
                        )
                    }
                }
            })
            return { queryParams: params }
        },
    },
}
</script>
