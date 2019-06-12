# reddit-streaming

## Prerequesites

- Reddit account for API credentials
- `sbt` installed
- 

## Usage 

In your bash/shell/terminal

```sh
export REDDIT_APPLICATION_ID="?"
export REDDIT_APPLICATION_TOKEN="?"

sbt assembly

# run on spark
spark-submit --class RedditDemo --master local[2] target/scala-2.11/reddit-streaming-assembly-0.0.1.jar spark
```

Add to your own project by adding this as a dependency in your `build.sbt`:

```java
libraryDependencies ++= Seq(
  //...
  "com.github.ruwai" %% "reddit-streaming" % "0.0.1",
  //...
)
```