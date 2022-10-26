import sys
from aws import Retriever, Processor, Poller

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Use arguments --help or -h to see usage.')
        sys.exit(1)
    if sys.argv[1] in ['--help', '-h']:
        print('Usage: python consumer.py <read_type> <read_location> <write_type> <write_location>')
        print('\tread_type: s3')
        print('\tread_location: bucket_name')
        print('\twrite_type: s3, dynamodb')
        print('\twrite_location: bucket_name, table_name')
        sys.exit(1)
    
    retriever = False
    processor = False

    read_type = sys.argv[1]
    read_location = sys.argv[2]

    if read_type == 's3':
        retriever = Retriever.S3Retriever(read_location)
    else:
        print('Invalid read_type argument.')
        sys.exit(1)
    
    write_type = sys.argv[3]
    write_location = sys.argv[4]

    if write_type == 's3':
        processor = Processor.S3Processor(write_location)
    elif write_type == 'dynamodb':
        processor = Processor.DynamoDBProcessor(write_location)

    if not retriever or not processor:
        print('There was an error setting up the retriever and processor.')
        sys.exit(1)

    else:
        poller = Poller.Poller(retriever, processor)
        poller.poll()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
