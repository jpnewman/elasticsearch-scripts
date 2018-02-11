# Sync Kibana Objects

Script ```sync_elasticsearch_objects.py``` can be used to download, upload, and delete the following Kibana objects: -

- Dashboards
- Visualizations
- Searches
- Templates

Objects can be filtered by adding ```include``` and ```exclude``` array of regular expression to the ```FOLDER_OBJECT_KEY_DICT``` values within script ```sync_elasticsearch_objects.py```.

## Install python requirements

~~~bash
pip install -r requirements.txt
~~~

## Arguments

It has the following positional arguments: -

|Variables|Description|Default|
|---|---|---|
|```elasticsearch_host```|Elasticsearch Host|http://10.10.10.10:9200|
|```--download```|Download from kibana|true|
|```--upload```|Uploads to kibana|false|
|```--reindex```|Reindex Elasticsearch to new indices and closes old indices|
|```--delete```|Delete from kibana|false|

## Setup

~~~
chmod u+x sync_elasticsearch_objects.py
~~~

### Download

Downloads objects and templates from remote kibana to local.

~~~
./sync_elasticsearch_objects.py http://elk-server:9200
~~~

~~~
./sync_elasticsearch_objects.py http://elk-server:9200 --download
~~~

### Upload

Uploads local objects and templates to remote kibana.

~~~
./sync_elasticsearch_objects.py http://elk-server:9200 --upload
~~~

### Reindex

Reindex All Elasticsearch indices

~~~
./sync_elasticsearch_objects.py http://elk-server:9200 --reindex '*'
~~~

Reindex Specific Elasticsearch indices

~~~
./sync_elasticsearch_objects.py http://elk-server:9200 --reindex 'artifactory-*'
~~~

### Delete

Deletes local objects and templates from remote kibana.

~~~
./sync_elasticsearch_objects.py http://elk-server:9200 --delete
~~~
