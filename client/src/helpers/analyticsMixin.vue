<script>
import {
    sentimentVsLabel,
    sentimentVsColor,
    countryVsColor,
    langVsLabel,
    usaCovidCurve,
    indiaCovidCurve,
    mexicoCovidCurve,
    vaccineHesistancyKeywords,
} from '@/helpers/constants'
import moment from 'moment'
export default {
    methods: {
        formatChartData(data) {
            if (data?.poi_name) {
                const poiBucketJSON = data.poi_name.buckets
                let poiChartDataArr = []
                poiBucketJSON.forEach((bucket) => {
                    poiChartDataArr.push({ name: bucket.val, y: bucket.count })
                })
                this.poiChartData.series[0].data = poiChartDataArr
            }
            if (data?.tweet_lang) {
                const tweetLangJSON = data.tweet_lang.buckets
                let tweetLangDataArr = []
                tweetLangJSON.forEach((bucket) => {
                    tweetLangDataArr.push({
                        name: langVsLabel[bucket.val],
                        y: bucket.count,
                    })
                })
                this.langChartData.series[0].data = tweetLangDataArr
            }
            if (data?.country) {
                const tweetcountryJSON = data.country.buckets
                let tweetcountryDataArr = []
                tweetcountryJSON.forEach((bucket) => {
                    tweetcountryDataArr.push({
                        name: bucket.val,
                        y: bucket.count,
                        color: countryVsColor[bucket.val],
                    })
                })
                this.countryChartData.series[0].data = tweetcountryDataArr
            }
            if (data?.sentiment) {
                let sentiments = data.sentiment.buckets || []
                let sentimentDataArr = []
                sentiments.forEach((bucket) => {
                    sentimentDataArr.push({
                        name: sentimentVsLabel[bucket.val],
                        y: bucket.count,
                        color: sentimentVsColor[bucket.val],
                    })
                })
                this.sentimentChartData.series[0].data = sentimentDataArr
            }
            if (data?.hashtags) {
                let hashtags = data.hashtags.buckets || []
                let hashtagDataArr = []
                hashtags.forEach((bucket) => {
                    hashtagDataArr.push({
                        name: bucket.val,
                        weight: bucket.count,
                    })
                })
                this.wordCloudData.series[0].data = hashtagDataArr
            }
            if (data?.tweet_date) {
                let tweetDates = data.tweet_date.buckets || []
                let tweetDateDataArr = []
                tweetDates.forEach((bucket) => {
                    if (moment(bucket.val).valueOf() > 1630468800000) {
                        tweetDateDataArr.push([
                            moment(bucket.val).valueOf(),
                            bucket.count,
                        ])
                    }
                })
                this.timeSeriesData.series[0].data = tweetDateDataArr
                    .sort((a, b) => {
                        return b[0] - a[0]
                    })
                    .reverse()
            }
        },

        formatVaccineChartData(data) {
            if (data?.time_with_sentiment) {
                let sentimentTweetDate =
                    data.time_with_sentiment['tweet_date,sentiment']
                let positiveDataArr = []
                let negativeDataArr = []
                let neutralDataArr = []
                sentimentTweetDate.forEach((bucket) => {
                    if (moment(bucket.value).valueOf() > 0) {
                        bucket.pivot.forEach((pi) => {
                            if (pi.value == 'positive') {
                                positiveDataArr.push([
                                    moment(bucket.value).valueOf(),
                                    pi.count,
                                ])
                            }
                            if (pi.value == 'negative') {
                                negativeDataArr.push([
                                    moment(bucket.value).valueOf(),
                                    pi.count,
                                ])
                            }
                            if (pi.value == 'neutral') {
                                neutralDataArr.push([
                                    moment(bucket.value).valueOf(),
                                    pi.count,
                                ])
                            }
                        })
                    }
                })
                positiveDataArr = positiveDataArr
                    .sort((a, b) => {
                        return b[0] - a[0]
                    })
                    .reverse()
                negativeDataArr = negativeDataArr
                    .sort((a, b) => {
                        return b[0] - a[0]
                    })
                    .reverse()
                neutralDataArr = neutralDataArr
                    .sort((a, b) => {
                        return b[0] - a[0]
                    })
                    .reverse()
                this.sentimentTimeSeriesData.series
                this.sentimentTimeSeriesData.series.push(
                    {
                        data: positiveDataArr,
                        name: 'Postive',
                        color: sentimentVsColor['positive'],
                    },
                    {
                        data: negativeDataArr,
                        name: 'Negative',
                        color: sentimentVsColor['negative'],
                    },
                    {
                        data: neutralDataArr,
                        name: 'Neutral',
                        color: sentimentVsColor['neutral'],
                    }
                )
            }

            if (data?.vaccine_countries) {
                let categories = []
                let vaccineByCountries = data.vaccine_countries
                let usaArr = []
                let indiaArr = []
                let mexicoArr = []
                vaccineByCountries.forEach((vC) => {
                    categories.push(vC.val)
                    for (let i = 0; i <= 6; i += 2) {
                        if (vC.country[i] == 'USA') {
                            usaArr.push(vC.country[i + 1])
                        } else if (vC.country[i] == 'India') {
                            indiaArr.push(vC.country[i + 1])
                        } else if (vC.country[i] == 'Mexico') {
                            mexicoArr.push(vC.country[i + 1])
                        }
                    }
                })

                let seriesData = []
                seriesData.push({ name: 'USA', data: usaArr })
                seriesData.push({ name: 'India', data: indiaArr })
                seriesData.push({ name: 'Mexico', data: mexicoArr })

                this.vaccineMentionsByCountryData.xAxis.categories = categories
                this.vaccineMentionsByCountryData.series = seriesData
            }

            if (data?.vaccine_sentiment) {
                let categories = []
                let vaccineBySentiment = data.vaccine_sentiment
                let neutralArr = []
                let negativeArr = []
                let positiveArr = []
                let vaccineHesistancyData = []
                vaccineBySentiment.forEach((vS) => {
                    categories.push(vS.val)

                    let positiveCount = 0
                    let negativeCount = 0
                    let neutralCount = 0
                    for (let i = 0; i <= 6; i += 2) {
                        if (vS.sentiment_score[i] == 'neutral') {
                            neutralArr.push(vS.sentiment_score[i + 1])
                            neutralCount = vS.sentiment_score[i + 1]
                        } else if (vS.sentiment_score[i] == 'negative') {
                            negativeArr.push(vS.sentiment_score[i + 1])
                            negativeCount = vS.sentiment_score[i + 1]
                        } else if (vS.sentiment_score[i] == 'positive') {
                            positiveArr.push(vS.sentiment_score[i + 1])
                            positiveCount = vS.sentiment_score[i + 1]
                        }
                    }

                    vaccineHesistancyData.push({
                        name: vS.val,
                        y:
                            (negativeCount /
                                (positiveCount +
                                    negativeCount +
                                    neutralCount)) *
                            100,
                    })
                })

                let seriesData = []
                seriesData.push({
                    name: 'Neutral',
                    data: neutralArr,
                    color: sentimentVsColor['neutral'],
                })
                seriesData.push({
                    name: 'Negative',
                    data: negativeArr,
                    color: sentimentVsColor['negative'],
                })
                seriesData.push({
                    name: 'Positive',
                    data: positiveArr,
                    color: sentimentVsColor['positive'],
                })

                this.vaccineCompaniesBySentimentData.xAxis.categories =
                    categories
                this.vaccineCompaniesBySentimentData.series = seriesData
                this.vaccineHesistancyChart.series[0].data =
                    vaccineHesistancyData
            }
            let usaCases = []
            let indiaCases = []
            let mexicoCases = []
            let usaPoiTweetsFinal = []
            let indiaPoiTweetsFinal = []
            let mexicoPoiTweetsFinal = []

            Object.keys(usaCovidCurve).forEach((record) => {
                usaCases.push([
                    moment(record).valueOf(),
                    parseInt(usaCovidCurve[record]),
                ])
            })
            let usaPOITweets =
                data?.US_covid_tweets?.facet_counts?.facet_ranges?.tweet_date
                    .counts
            let indiaPOITweets =
                data?.India_covid_tweets?.facet_counts?.facet_ranges?.tweet_date
                    .counts
            let mexPOITweets =
                data?.Mexico_covid_tweets?.facet_counts?.facet_ranges
                    ?.tweet_date.counts
            for (let i = 0; i < usaPOITweets.length; i += 2) {
                if (moment(usaPOITweets[i]).valueOf() < 1632369600000) {
                    usaPoiTweetsFinal.push([
                        moment(usaPOITweets[i]).valueOf(),
                        usaPOITweets[i + 1],
                    ])
                }
            }
            for (let i = 0; i < indiaPOITweets.length; i += 2) {
                if (moment(indiaPOITweets[i]).valueOf() < 1632369600000) {
                    indiaPoiTweetsFinal.push([
                        moment(indiaPOITweets[i]).valueOf(),
                        indiaPOITweets[i + 1],
                    ])
                }
            }
            for (let i = 0; i < mexPOITweets.length; i += 2) {
                if (moment(mexPOITweets[i]).valueOf() < 1632369600000) {
                    mexicoPoiTweetsFinal.push([
                        moment(mexPOITweets[i]).valueOf(),
                        mexPOITweets[i + 1],
                    ])
                }
            }
            Object.keys(indiaCovidCurve).forEach((record) => {
                indiaCases.push([
                    moment(record).valueOf(),
                    parseInt(indiaCovidCurve[record]),
                ])
            })
            Object.keys(mexicoCovidCurve).forEach((record) => {
                mexicoCases.push([
                    moment(record).valueOf(),
                    parseInt(mexicoCovidCurve[record]),
                ])
            })
            this.covidVsPoiUSACurve.series[0].data = usaCases
            this.covidVsPoiUSACurve.series[1].data = usaPoiTweetsFinal

            this.covidVsPoiIndiaCurve.series[0].data = indiaCases
            this.covidVsPoiIndiaCurve.series[1].data = indiaPoiTweetsFinal

            this.covidVsPoiMexicoCurve.series[0].data = mexicoCases
            this.covidVsPoiMexicoCurve.series[1].data = mexicoPoiTweetsFinal

            let hesKeywords = []
            Object.keys(vaccineHesistancyKeywords).forEach((key) => {
                hesKeywords.push({
                    name: key,
                    weight: vaccineHesistancyKeywords[key],
                })
            })
            this.vaccineHesistancyWordCloudData.series[0].data = hesKeywords
        },
    },
}
</script>
