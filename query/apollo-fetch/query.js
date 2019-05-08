import { createApolloFetch } from 'apollo-fetch'
import gql from 'graphql-tag'

const timeLineServiceUrl = "..."
const authToken = "..."

const apolloFetch = createApolloFetch({ uri: timeLineServiceUrl });

apolloFetch.use(({ request, options }, next) => {
  options.headers = {
    "authorization": `Bearer ${authToken}`
  }
  next()
})

async function timeLineQuery1(tenantId, input) {
    const query = gql`
        query timeLineQuery1($tenantId: ID!, $input: TimeLineQueryInput!) {
            timeLineForQuery(tenantId: $tenantId, input: $input) {
                id
                createdOn
                createdBy
                events {
                    score
                    event {
                        id
                        externalId
                        type {
                            id
                            anem
                        }
                        content
                        startedOn
                    }
                }
            }
        }
    }`

    const variables = {
        tenantId: tenantId,
        input: input
    }

    const { data, errors, extensions } = await apolloFetch({ query, variables })

    if (errors) throw new Error(errors[0].message)

    if (data && data.timeLineForQuery) {
        return data.timeLineForQuery
    }

    return null
}

//
// GQL Fragments
//
const TimeLineDetailsFragment = gql`
  fragment TimeLineDetails on TimeLine {
    id
    createdOn
    createdBy
    events {
      score
      event {
        id
        externalId
        type {
            id
            anem
        }
        content
        startedOn
      }
    }
  }
`

async function timeLineQuery2(tenantId, input) {

    const query = gql`
      query timeLineQuery2($tenantId: ID!, $input: TimeLineQueryInput!) {
        timeLineForQuery(tenantId: $tenantId, id: $kindId, name: $kindName) {
          ...TimeLineDetails
        }
      }
      ${TimeLineDetailsFragment}
    `

    const variables = {
        tenantId: tenantId,
        input: input
    }

    const { data, errors, extensions } = await apolloFetch({ query, variables })

    if (errors) throw new Error(JSON.stringify(errors))

    if (data && data.timeLineForQuery) {
      return data.timeLineForQuery
    } 
    
    return null
}


