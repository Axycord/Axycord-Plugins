package mmaarij.axycord.lastfm

import org.junit.Assert.*
import org.junit.Test

class ActivityTextTest {
    @Test fun `ordinary labels are retained`() {
        assertEquals("Artist - Song", fitActivityText("Artist - Song"))
    }

    @Test fun `short labels use invisible unicode padding rather than mojibake`() {
        assertEquals("A\u200B", fitActivityText("A"))
        assertEquals("\u200B\u200B", fitActivityText(""))
    }

    @Test fun `long labels respect the maximum without splitting emoji`() {
        assertEquals(128, fitActivityText("a".repeat(129)).length)
        assertEquals("a".repeat(127), fitActivityText("a".repeat(127) + "\uD83D\uDE00"))
        assertEquals("a".repeat(126) + "\uD83D\uDE00", fitActivityText("a".repeat(126) + "\uD83D\uDE00"))
    }
}
