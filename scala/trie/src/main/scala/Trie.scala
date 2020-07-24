package example

import scala.collection.mutable.ArrayBuffer
import scala.collection.Iterator

class Trie[T](var root: Node[T] = new Node[T]) {
  def find(key: String): Option[T] = {
    var node = root
    for (char <- key) {
      node.children.get(char) match {
        case Some(child) => {
          node = child
        }
        case None => {
          return None
        }
      }
    }
    node.value
  }

  def insert(key: String, value: T): Unit = {
    var node = root
    for (char <- key) {
      node = node.children.getOrElseUpdate(char, new Node[T])
    }
    node.value = Some(value)
  }

  def keys(): Array[String] = {
    var node_stack = new ArrayBuffer[Node[T]]
    node_stack += root

    var iter_stack = new ArrayBuffer[Iterator[Char]]
    var char_stack = new ArrayBuffer[Char]

    var keys = new ArrayBuffer[String]

    do {
      val node = node_stack.last

      if (iter_stack.length == 0) {
        iter_stack += node.children.keys.iterator
      }

      var iter = iter_stack.last

      if (iter.hasNext) {
        val char = iter.next
        char_stack += char
        node.children.get(char).map(child => {
            node_stack += child
            iter_stack += child.children.keys.iterator
        })
      } else {
        node.value.map(_ => {
            keys += char_stack.mkString("")
        })
        if (node_stack.length > 0) {
            node_stack.remove(node_stack.length - 1)
        }
        if (iter_stack.length > 0) {
            iter_stack.remove(iter_stack.length - 1)
        }
        if (char_stack.length > 0) {
            char_stack.remove(char_stack.length - 1)
        }
      }
    } while (char_stack.length > 0)
    keys.toArray
  }
}
