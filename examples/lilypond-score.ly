\version "2.18"
\language "français"

\header {
  tagline = ""
  composer = ""
}

MetriqueArmure = {
  \tempo 2.=50
  \time 6/4
  \key sib \major
}

italique = { \override Score . LyricText #'font-shape = #'italic }

roman = { \override Score . LyricText #'font-shape = #'roman }

MusiqueCouplet = \relative do' {
  \partial 2. re4\p re^"Solo" re
  sol2. la2 la4
  sib2 sib4 \breathe
  la4 sib la
  sol2. \acciaccatura {la16[ sol]} fad2 sol4
  la2 r4 re,2 re4
  sol2 sol4 la\< sol la
  sib2\! \acciaccatura {la16[ sol]} fa4 \breathe sib2 do4
  re2 do4 sol2 la4
  sib2. ~ sib2 \bar "||"
}

MusiqueRefrainI = \relative do'' {
  re4\f^"Chœur"
  re2 do4 sib2 la4
  sol2. fad2 \breathe re4
  sol2 la4 sib2 do4
  re2.~ re4 \oneVoice r \voiceOne re\f
  re2 do4 sib2 la4
  sol2. fad2 \oneVoice r4 \voiceOne
  sol2 la4\< sib la sol\!
  la2. sib2( la4)
  sol2.\fermata \bar "|."
}

MusiqueRefrainII = \relative do'' {
  sib4
  sib2 la4 sol2 re4
  mib4 re dod re2 do4
  sib2 re4 sol2 sol4
  fad2.~ fad4 s sib4
  sib2 la4 sol2 re4
  mib4 re dod re2 s4
  sib2 do4 re do sib
  do2. re2( do4)
  sib2.
}

ParolesCouplet = \lyricmode {
  Le soir é -- tend sur la Ter -- re
  Son grand man -- teau de ve -- lours,
  Et le camp, calme et so -- li -- tai -- re,
  Se re -- cueille en ton a -- mour.
}

ParolesRefrain = \lyricmode {
  \italique
  Ô Vier -- ge de lu -- miè -- re,
  É -- toi -- le de nos cœurs,
  En -- tends no -- tre pri -- è -- re,
  No -- tre_- Da -- me des É -- clai -- reurs_!
}

\score{
  <<
    \new Staff <<
      \set Staff.midiInstrument = "flute"
      \set Staff.autoBeaming = ##f
      \new Voice = "couplet" {
        \override Score.PaperColumn #'keep-inside-line = ##t
        \MetriqueArmure
        \MusiqueCouplet
        \voiceOne
        \MusiqueRefrainI
      }
        \new Voice = "refrainII" {
          s4*50
          \voiceTwo
          \MusiqueRefrainII
        }
    >>
    \new Lyrics \lyricsto couplet {
      \ParolesCouplet
      \ParolesRefrain
    }
  >>
  \layout{}
  \midi{}
}
