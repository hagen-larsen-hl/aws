import sys
from tools import Retriever, Processor, Poller

def main(args):
    if len(args) == 1:
        raise Exception('Use arguments --help or -h to see usage.')

    elif args[1] == '--help' or args[1] == '-h':
        print('Usage: python consumer.py <read_type> <read_location> <write_type> <write_location>')
        print('\tread_type: s3, sqs')
        print('\tread_location: bucket_name, queue_name')
        print('\twrite_type: s3, dynamodb')
        print('\twrite_location: bucket_name, table_name')
        sys.exit(0)
    
    elif len(args) != 5:
        raise Exception('Incorrect number of arguments. Use arguments --help or -h to see usage.')

    retriever = False
    processor = False

    read_type = args[1]
    read_location = args[2]

    if read_type == 's3':
        retriever = Retriever.S3Retriever(read_location)
    elif read_type == 'sqs':
        retriever = Retriever.SQSRetriever(read_location)
    else:
        raise Exception('Invalid read_type')
    
    write_type = args[3]
    write_location = args[4]

    if write_type == 's3':
        processor = Processor.S3Processor(write_location)
    elif write_type == 'dynamodb':
        processor = Processor.DynamoDBProcessor(write_location)
    else:
        raise Exception('Invalid write_type')

    if not retriever or not processor:
        raise Exception('There was an error setting up the retriever or processor.')

    else:
        poller = Poller.Poller(retriever, processor)
        poller.poll()

if __name__ == '__main__':
    main(sys.argv)
