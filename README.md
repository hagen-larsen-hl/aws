# **Consumer Program**

## **Overview**

The consumer program accepts four parameters:
1. retrieval source type - *s3*
2. retrieval source name - *bucket name*
3. process destination type - *s3, dynamodb*
4. process destination name - *bucket name, table name*

 The responsibilities of this program are divided primarily into three objects - a **Poller**, a **Retriever**, and a **Processor**.

![class diagram](docs/classDiagram.png)


### **Poller**
The poller manages the looping nature of the program. Composed of both a retriever and processor, the poller instructs the retriever to retrieve and, if needed, the processor to process the retrieved request. If no request is retrieved, the poller awaits a specified timeout duration and tries again. In the case of 5 consecutive failed retrievals, the program exits.

### **Retriever**
Using Boto3, the retriever obtains JSON requests from the specified source. It uses a **WidgetRequestFactory** to translate the request from JSON to a **Request** object and returns it to the poller.

### **Processor**
The processor obtains the request object and determines the request type. Currently, only *create* is supported. The processor then processes the request according to its type. In the case of a create request, the item is uploaded to the specified resource via Boto3.

## **Additional Visualization**

![flow chart](docs/flowChart.png)