import axios from 'axios'

const http = axios.create({
    baseURL: 'https://payable-neda-aashiq-192277fe.koyeb.app/',
    headers: {
        'Content-type': 'application/json',
    },
})

http.interceptors.request.use(
    (request) => {
        return request
    },
    (error) => {
        throw error
    }
)

http.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        // Unauthorized
        if (error === 401) {
            console.log(error)
        } else {
            throw error
        }
    }
)

export default http
