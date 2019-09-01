module.exports = async function(context, eventHubMessages) {
  eventHubMessages.forEach((message, index) => {
    context.log(
      `Processed notification ${index} of ${eventHubMessages.length}: ${JSON.stringify(message, null, 2)}`
    );
  });
};
