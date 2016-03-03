# simplePipeline
pipeline process example

Hi everyone

This is a simple pipeline python package. "S3P"
S3P shall show how to implement applications where we have at least 2 major things:
1 - sequence handling of something
2 - periodicity of handling

For example we have case where we shall do something with incoming files on ftp server.
Files are coming periodicity every 5 sec....
We need to do a sequence of handling like - take avery file by filter, extract necessary info and save it to DB.

In this case S3P is good enough here.

 |->IN->filter->extracting->saving->|
 |                                  |
 |----------- LOOP ---------------<-|

Solution:
 We have to develop basic module: pipeline. Actually we need basic pipeline module class - PipelineModule
 if we need filter module or saving to DB module - then those modules shall be inheriting from PipelineModule
 We need pipeline container where those modules shall do something according to their purposes.
 So, this is Pipeline class. OK.
 There are help modules: pylib, yamlloader, log. They don't do something for business logic.
 There are several pipeline modules input / output showing main process.
 app - this is application and it is example how to do pipeline applications. it is single process application and
 we don't do multiprocessing or maltreating there. Actually it can be done later but it depends on business logic.

