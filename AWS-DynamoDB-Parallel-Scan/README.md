# Parallel Scan DynamoDB


Current Code is set to read 10 segments Parallelly

You can change it according to your needs

## Scan Method
The scan method returns a subset of the items each time, called a page. The LastEvaluatedKey value in the response is then passed to the scan method via the ExclusiveStartKey parameter. When the last page is returned, LastEvaluatedKey is not part of the response

## ProjectionExpression
ProjectionExpression specifies the attributes you want in the scan result

## FilterExpression
FilterExpression specifies a condition that returns only items that satisfy the condition. All other items are discarded.

## TotalSegments (integer)
For a parallel Scan request, TotalSegments represents the total number of segments into which the Scan operation will be divided. The value of TotalSegments corresponds to the number of application workers that will perform the parallel scan. For example, if you want to use four application threads to scan a table or an index, specify a TotalSegments value of 4.

The value for TotalSegments must be greater than or equal to 1, and less than or equal to 1000000. If you specify a TotalSegments value of 1, the Scan operation will be sequential rather than parallel.

If you specify TotalSegments , you must also specify Segment .

## Segment (integer)
For a parallel Scan request, Segment identifies an individual segment to be scanned by an application worker.

Segment IDs are zero-based, so the first segment is always 0. For example, if you want to use four application threads to scan a table or an index, then the first thread specifies a Segment value of 0, the second thread specifies 1, and so on.

The value of LastEvaluatedKey returned from a parallel Scan request must be used as ExclusiveStartKey with the same segment ID in a subsequent Scan operation.

The value for Segment must be greater than or equal to 0, and less than the value provided for TotalSegments .

If you provide Segment , you must also provide TotalSegments .

## Note

**ExpressionAttributeNames**:  ExpressionAttributeNames provides name substitution. We use this because year is a reserved word in DynamoDB—you can't use it directly in any expression, including KeyConditionExpression. You can use the expression attribute name #yr to address this.

**ExpressionAttributeValues**: ExpressionAttributeValues provides value substitution. You use this because you can't use literals in any expression, including KeyConditionExpression. You can use the expression attribute value :yyyy to address this.
