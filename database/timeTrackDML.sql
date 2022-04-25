/* Draft queries */


/* Multiplies the cost of a task */ 
SELECT  Tasks.taskDescription, 
        CAST(Tasks.taskTime * projects.projectBillRate AS DECIMAL(5,2)) as totalCost 
FROM Tasks 
JOIN projects 
ON Tasks.projectId = projects.projectId;
