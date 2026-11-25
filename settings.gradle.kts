pluginManagement {
    providers.gradleProperty("axycordCheckout").orNull?.let { path ->
        includeBuild(file(path).resolve("plugin-gradle"))
    }
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven("https://raw.githubusercontent.com/Axycord/Axycord/maven") {
            content { includeGroupByRegex("mmaarij\\.axycord(\\..*)?") }
        }
    }
    plugins { id("mmaarij.axycord.plugin") version "1.0.0" }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven("https://raw.githubusercontent.com/Axycord/Axycord/maven") {
            content { includeGroup("mmaarij.axycord") }
        }
    }
}

rootProject.name = "axycord-plugins"
include(":platformindicators", ":emojireplace", ":permissionsviewer")
