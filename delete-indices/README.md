
# Delete Indices based on status

Delete elasticsearch indices by status.

# References

- <http://elasticsearch-py.readthedocs.io/en/master/api.html>

## Install python requirements

~~~bash
pip install -r requirements.txt
~~~

## Run

> Change access permissions

~~~
chmod u+x delete-indices.py
~~~

### Delete closed indices

~~~
./delete-indices.py elk-server:9200
~~~

### Dry-Run

~~~
./delete-indices.py elk-server:9200 --dry-run
~~~

### Delete open indices

~~~
./delete-indices.py elk-server:9200 -s open --dry-run
~~~

### Delete all indices

~~~
./delete-indices.py elk-server:9200 -s all --dry-run
./delete-indices.py elk-server:9200 -s none --dry-run
~~~

### Delete specific indices

~~~
./delete-indices.py elk-server:9200 --index-names index-2017.01.22 --dry-run
./delete-indices.py elk-server:9200 -n index-2017.01.21 index-2017.01.22 --dry-run
~~~

## Lint python script

~~~
flake8 **/*.py
~~~

## Code Metrics

~~~
radon cc . -a -nc
~~~

## UnitTest

~~~
py.test --html=report.html
~~~

## Line Count

~~~
find . -name '*.py' | xargs wc -l
~~~

## License

MIT / BSD

## Author Information

John Paul Newman
