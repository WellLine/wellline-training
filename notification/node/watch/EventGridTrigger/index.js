module.exports = async function (context, eventGridEvent) {
    context.log(
        `Processed notification: ${JSON.stringify(eventGridEvent, null, 2)}`
      );
  };