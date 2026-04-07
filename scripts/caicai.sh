#!/bin/bash
# Caicai — pet your cat in the terminal
# Usage: caicai or source this in your .zshrc as an alias

MEOWS=("miao~" "miao!" "miao miao~" "purr~" "nya~" "miao?" "~miao~")
HEARTS=("❤️" "💕" "💖" "🩷" "♥️")
MEOW=${MEOWS[$((RANDOM % ${#MEOWS[@]}))]}

# Random hearts
H1=${HEARTS[$((RANDOM % ${#HEARTS[@]}))]}
H2=${HEARTS[$((RANDOM % ${#HEARTS[@]}))]}
H3=${HEARTS[$((RANDOM % ${#HEARTS[@]}))]}

cat << CAICAI

        $H1  $H2  $H3
    /\\_/\\
   ( ^.^ )  $MEOW
    > ^ <
   /|   |\\
  (_|   |_)

CAICAI

# Play meow sound (macOS)
afplay /System/Library/Sounds/Pop.aiff 2>/dev/null &
