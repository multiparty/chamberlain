-- --------------------------------------------------------------------------------------------------------
-- Datasets 
-- Columns : DatasetId, datasetSchema 
-- --------------------------------------------------------------------------------------------------------
INSERT INTO chamberlain.datasets VALUES ("HRI0","a,b,c,keeprows");
INSERT INTO chamberlain.datasets VALUES ("HRI1","d,e,f,keeprows");

-- --------------------------------------------------------------------------------------------------------
-- Workflows
-- Columns : workflowId, operationName
-- --------------------------------------------------------------------------------------------------------
INSERT INTO chamberlain.workflows VALUES ("WK001","SUM");
INSERT INTO chamberlain.workflows VALUES ("WK002","MEAN");
INSERT INTO chamberlain.workflows VALUES ("WK003","STD_DEV");

-- --------------------------------------------------------------------------------------------------------
-- Cardinals
-- Columns: cardinalId, cardinalIp
-- Change these IP addresses according to your deployments
-- --------------------------------------------------------------------------------------------------------
INSERT INTO chamberlain.cardinals VALUES ("cardinal001","12.34.45.67:80");
INSERT INTO chamberlain.cardinals VALUES ("cardinal002","123.53.45.67:80");
INSERT INTO chamberlain.cardinals VALUES ("cardinal003","12.567.45.98:80");

-- --------------------------------------------------------------------------------------------------------
-- Storage Relationships
-- Columns: storageRelationshopId, datasetId, cardinalId1, cardinalId2, cardinalId3
-- Change the ordering of the cardinals based on which cardinal has party 1, party 2 and party 3 shares
-- --------------------------------------------------------------------------------------------------------
INSERT INTO chamberlain.storageRelationships VALUES ("ST001","HR0","cardinal001","cardinal002","cardinal003");
INSERT INTO chamberlain.storageRelationships VALUES ("ST002","HR1","cardinal001","cardinal002","cardinal003");

--------------------------------------------------------------------------------------------------------
-- Workflow Relationships
-- Columns: workflowRelationshipId, datasetId, workflowId
--------------------------------------------------------------------------------------------------------
INSERT INTO chamberlain.workflowRelationships VALUES ("WR001","HR0","WK001");
INSERT INTO chamberlain.workflowRelationships VALUES ("WR002","HR0","WK002");
INSERT INTO chamberlain.workflowRelationships VALUES ("WR003","HR0","WK003");
INSERT INTO chamberlain.workflowRelationships VALUES ("WR004","HR1","WK001");
INSERT INTO chamberlain.workflowRelationships VALUES ("WR005","HR1","WK002");
INSERT INTO chamberlain.workflowRelationships VALUES ("WR006","HR1","WK003");

