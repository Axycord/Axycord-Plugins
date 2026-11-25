package mmaarij.axycord.lastfm

/** Keep activity labels within the host's limits without splitting an emoji surrogate pair. */
internal fun fitActivityText(value: String): String {
    var text = value.take(128)
    if (text.lastOrNull()?.isHighSurrogate() == true) text = text.dropLast(1)
    return text + "\u200B".repeat((2 - text.length).coerceAtLeast(0))
}
