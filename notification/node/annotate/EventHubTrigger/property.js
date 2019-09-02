const CognitiveServicesCredentials = require("@azure/ms-rest-js");
const TextAnalyticsAPIClient = require("@azure/cognitiveservices-textanalytics");

const subscription_key = process.env['TEXT_ANALYTICS_KEY']
const endpoint = process.env['TEXT_ANALYTICS_ENDPOINT']

console.log(`subscription_key: ${subscription_key}`)
console.log(`endpoint: ${endpoint}`)

const creds = new CognitiveServicesCredentials.ApiKeyCredentials({ inHeader: { 'Ocp-Apim-Subscription-Key': subscription_key } });
const client = new TextAnalyticsAPIClient.TextAnalyticsClient(creds, endpoint);

module.exports.updateEventLanguage = async function(srcEvent, eventUpdate) {

  if (srcEvent.content && srcEvent.content.length > 0) {
    const inputDocuments = {
      documents: [
          { id: "1", text: srcEvent.content }
      ]
    }

    const result = await client.detectLanguage({
      languageBatchInput: inputDocuments
    })

    // console.log(`Result: ${JSON.stringify(result)}`)

    if (result && result.documents && result.documents.length > 0) {
      const doc0 = result.documents[0]
      if (doc0.detectedLanguages && doc0.detectedLanguages.length > 0) {
        const lang0 = doc0.detectedLanguages[0]
        // console.log(`Detect Language: ${JSON.stringify(lang0)}`)
        eventUpdate.addProperties = [{ name:"iso6391", "value": lang0.iso6391Name || '' }]
      }
    }
  }
}