import org.scalatest._
import example.Trie

class TrieSpec extends FunSuite with DiagrammedAssertions {
    test("Construct hello world trie") {
        var t = new Trie[String]
        t.insert("hello", "world")
        t.insert("hockey", "stick")
        assert(t.find("hello") == Some("world"))
        assert(t.find("hockey") == Some("stick"))
    }

    test("get trie keys") {
        var t = new Trie[String]
        t.insert("hello", "world")
        t.insert("hey", "you")
        t.insert("hockey", "stick")
        val v = t.keys
        assert(v === Array("hello", "hey", "hockey"))
    }

    test("test empty trie") {
        var t = new Trie[String]
        val v = t.keys
        println(v.length)
        assert(v === Array())
    }

    test("test single key trie") {
        var t = new Trie[String]
        t.insert("hello", "world")
        val v = t.keys
        println(v.length)
        assert(v === Array("hello"))
    }
}