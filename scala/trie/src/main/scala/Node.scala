package example

import scala.collection.mutable.TreeMap

class Node[T](
    var children: TreeMap[Char, Node[T]] = new TreeMap[Char, Node[T]],
    var value: Option[T] = None
)
