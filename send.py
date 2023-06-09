# import asyncio
# from azure.servicebus.aio import ServiceBusClient
# from azure.servicebus import ServiceBusMessage
# # from azure.identity.aio import DefaultAzureCredential
# from azure.identity import ManagedIdentityCredential
# from azure.identity import ClientSecretCredential
# from azure.identity.aio import ManagedIdentityCredential

# NAMESPACE_CONNECTION_STR = "Endpoint=sb://dayinhistory.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=cMuWaU+sXBo8C1HnLgHVvhI44Me3tV3mO+ASbAumJr8="
# FULLY_QUALIFIED_NAMESPACE = "dayInHistory.servicebus.windows.net"
# ARTICLE_QUEUE_NAME = "articlequeue"
# HEADLINE_QUEUE_NAME = "headlinequeue"

# # credential = DefaultAzureCredential(managed_identity_client_id=client_id)
# credential = ClientSecretCredential(
#     tenant_id="ece491a0-b5f1-432c-8b09-315e81d41ce5",
#     client_id="75f0f23b-d5a0-4523-9a52-c419bdf103c5",
#     client_secret="HEO8Q~mxUQBl0qilbC4~8IrDyrD8gcYxbqUOHdjl",
# )


# async def send_single_message(sender):
#     # Create a Service Bus message and send it to the queue
#     message = ServiceBusMessage("Single Message")
#     await sender.send_messages(message)
#     print("Sent a single message")
# async def send_a_list_of_messages(sender):
#     # Create a list of messages and send it to the queue
#     messages = [ServiceBusMessage("Message in list") for _ in range(5)]
#     await sender.send_messages(messages)
#     print("Sent a list of 5 messages")

# async def send_batch_message(sender):
#     # Create a batch of messages
#     async with sender:
#         batch_message = await sender.create_message_batch()
#         for _ in range(10):
#             try:
#                 # Add a message to the batch
#                 batch_message.add_message(ServiceBusMessage("Message inside a ServiceBusMessageBatch"))
#             except ValueError:
#                 # ServiceBusMessageBatch object reaches max_size.
#                 # New ServiceBusMessageBatch object can be created here to send more data.
#                 break
#         # Send the batch of messages to the queue
#         await sender.send_messages(batch_message)
#     print("Sent a batch of 10 messages")

# async def run():
#     # create a Service Bus client using the connection string
#     async with ServiceBusClient.from_connection_string(
#         conn_str=NAMESPACE_CONNECTION_STR,
#         logging_enable=True) as servicebus_client:
#         # Get a Queue Sender object to send messages to the queue
#         sender = servicebus_client.get_queue_sender(queue_name=HEADLINE_QUEUE_NAME)
#         async with sender:
#             # Send one message
#             await send_single_message(sender)
#             # Send a list of messages
#             await send_a_list_of_messages(sender)
#             # Send a batch of messages
#             await send_batch_message(sender)

# asyncio.run(run())
# print("Done sending messages")
# print("-----------------------")