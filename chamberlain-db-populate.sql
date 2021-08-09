-- --------------------------------------------------------------------------------------------------------
-- Datasets 
-- Columns : pid, datasetId, datasetSchema, backend, parameters, description
-- --------------------------------------------------------------------------------------------------------
INSERT INTO `datasets` VALUES (1,'HRI0','a,b,c,keeprows','jiff','{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, "decimalDigits": 0, "ZP": 16777729}','no description');
INSERT INTO `datasets` VALUES (2,'HRI0','a,b,c,keeprows','jiff','{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, "decimalDigits": 0, "ZP": 16777729}','no description');
INSERT INTO `datasets` VALUES (3,'HRI0','a,b,c,keeprows','jiff','{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, "decimalDigits": 0, "ZP": 16777729}','no description');
INSERT INTO `datasets` VALUES (3,'HRI1','d,e,f,keeprows','jiff','{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, "decimalDigits": 0, "ZP": 16777729}','no description');
INSERT INTO `datasets` VALUES (2,'HRI1','d,e,f,keeprows','jiff','{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, "decimalDigits": 0, "ZP": 16777729}','no description');
INSERT INTO `datasets` VALUES (1,'HRI1','d,e,f,keeprows','jiff','{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, "decimalDigits": 0, "ZP": 16777729}','no description');

-- --------------------------------------------------------------------------------------------------------
-- Workflows
-- Columns : workflowId, operationName. datasetId, sourceBucket, sourceKey, description
-- --------------------------------------------------------------------------------------------------------
INSERT INTO `workflows` VALUES ('WK001','std_dev','HRI0','curia-test','workflows/HRI0/std_dev_HRI0.py','no description');
INSERT INTO `workflows` VALUES ('WK002','sum','HRI0','curia-test','workflows/HRI0/sum_HRI0.py','no description');
INSERT INTO `workflows` VALUES ('WK003','mean','HRI0','curia-test','workflows/HRI0/mean_HRI0.py','no description');
INSERT INTO `workflows` VALUES ('WK004','mean','HRI1','curia-test','workflows/HRI1/mean_HRI1.py','no description');
INSERT INTO `workflows` VALUES ('WK005','sum','HRI1','curia-test','workflows/HRI1/sum_HRI1.py','no description');
INSERT INTO `workflows` VALUES ('WK006','std_dev','HRI1','curia-test','workflows/HRI1/std_dev_HRI1.py','no description');

-- --------------------------------------------------------------------------------------------------------
-- Cardinals
-- Columns: cardinalId, cardinalIp, description
-- Change these IP addresses according to your deployments
-- --------------------------------------------------------------------------------------------------------
INSERT INTO `cardinals` VALUES ('cardinal001','http://34.139.197.119:80','no description');
INSERT INTO `cardinals` VALUES ('cardinal002','http://a4c680c558a854e3388375a19f09fcea-1087590076.us-east-1.elb.amazonaws.com:5000','no description');
INSERT INTO `cardinals` VALUES ('cardinal003','http://52.224.188.74:5000','no description');

-- --------------------------------------------------------------------------------------------------------
-- Storage Relationships
-- Columns: storageRelationshopId, datasetId, cardinals, description
-- Change the ordering of the cardinals based on which cardinal has party 1, party 2 and party 3 shares
-- --------------------------------------------------------------------------------------------------------
INSERT INTO `storageRelationships` VALUES ('ST001','HRI0','cardinal001,cardinal002,cardinal003','no description');
INSERT INTO `storageRelationships` VALUES ('ST002','HRI1','cardinal001,cardinal002,cardinal003','no description');

--------------------------------------------------------------------------------------------------------
-- Workflow Relationships
-- Columns: workflowRelationshipId, datasetId, workflowId, description
--------------------------------------------------------------------------------------------------------
INSERT INTO `workflowRelationships` VALUES ('WR001','HR0','WK001','no description');
INSERT INTO `workflowRelationships` VALUES ('WR002','HR0','WK002','no description');
INSERT INTO `workflowRelationships` VALUES ('WR003','HR0','WK003','no description');
INSERT INTO `workflowRelationships` VALUES ('WR004','HR1','WK004','no description');
INSERT INTO `workflowRelationships` VALUES ('WR005','HR1','WK005','no description');
INSERT INTO `workflowRelationships` VALUES ('WR006','HR1','WK006','no description');

