:- dynamic song_attribute/2.


song(kimada_nawe, clarence_wijewardena, [electric_guitar, bass, drums, organ], 130, melodic, 1974).
song(ganga_addara, vijaya_kumaratunga, [acoustic_guitar, flute, violin, tabla], 80, melodic, 1980).
song(master_sir, nanda_malini, [piano, violin, acoustic_guitar], 70, narrative, 1978).
song(sasara_wasana_thuru, wd_amaradeva, [sitar, tabla, serpina, violin], 65, classical_melodic, 1970).
song(siri_sangabodhi, bns, [synthesizer, drum_machine, electric_guitar, bass], 135, clean, 2002).
song(mango_kalu_nande, annesley_malewana, [acoustic_guitar, bongos, bass], 140, upbeat, 1969).
song(meedum_gala_kande, hr_jothipala, [violin, mandolin, tabla, flute], 110, melodic, 1976).
song(eda_rea, milton_mallawarachchi, [piano, violin, acoustic_guitar, bass, drums], 75, soulful, 1978).
song(mee_wadayaki_jeevithe, ct_fernando, [acoustic_guitar, tabla], 120, narrative, 1965).
song(bambara_pahasa, rookantha_gunathilake, [synthesizer, electric_guitar, saxophone, bass, drums], 115, clean, 1989).
song(mal_mitak_thiyanna, kasun_kalhara, [piano, acoustic_guitar, violin, cello], 68, soulful, 2005).
song(chandrayan_pidu, daddy, [electric_guitar, acoustic_guitar, bass, drums], 90, clean, 2009).
song(rambari, lahiru_perera, [synthesizer, drum_machine, sampler, bass], 130, energetic, 2009).
song(sandawathiye, ridma_weerawardena, [acoustic_guitar, flute, tabla, bass], 100, melodic, 2018).
song(re_ahase, billy_fernando, [drums, acoustic_guitar, bass, piano], 125, upbeat, 2017).



recommend_genre('70s Sinhala Pop', 0.95, 'Signature sound of the 70s with organ, clean electric guitar, and a melodic style.') :-
    song_attribute(year, Year), Year >= 1970, Year < 1980,
    song_attribute(bpm, BPM), BPM => 120,
    song_attribute(instruments, Inst), has_instrument(organ, Inst).

recommend_genre('Baila', 0.98, 'Very high tempo with characteristic trumpet and percussion, designed for dancing.') :-
    song_attribute(bpm, BPM), BPM >= 150,
    song_attribute(vocals, 'energetic'),
    song_attribute(instruments, Inst),
    once((has_instrument(trumpet, Inst); has_instrument(bongos, Inst))).

recommend_genre('80s Pop Rock', 0.90, 'Blend of pop and rock with synthesizers, common in the late 80s.') :-
    song_attribute(year, Year), Year >= 1985, Year < 1995,
    song_attribute(instruments, Inst), has_instrument(synthesizer, Inst), has_instrument(electric_guitar, Inst).

recommend_genre('Sri Lankan Classical Folk', 0.96, 'Slow tempo with traditional Eastern instruments like Sitar and Tabla.') :-
    song_attribute(bpm, BPM), BPM =< 70,
    song_attribute(vocals, 'classical_melodic'),
    song_attribute(instruments, Inst),
    once((has_instrument(sitar, Inst); has_instrument(serpina, Inst))).

recommend_genre('Narrative Folk', 0.92, 'Slow, story-telling song, often from a film soundtrack with orchestral elements.') :-
    song_attribute(bpm, BPM), BPM =< 75,
    song_attribute(vocals, 'narrative'),
    song_attribute(instruments, Inst),
    once((has_instrument(piano, Inst); has_instrument(violin, Inst))).

recommend_genre('Calypso Pop', 0.94, 'Upbeat tempo with characteristic Calypso percussion (bongos) from the 60s/70s.') :-
    song_attribute(year, Year), Year < 1975,
    song_attribute(bpm, BPM), BPM >= 135,
    song_attribute(vocals, 'upbeat'),
    song_attribute(instruments, Inst), has_instrument(bongos, Inst).

recommend_genre('Modern Folk Fusion', 0.93, 'A modern (post-2010) blend of traditional Eastern and Western instruments.') :-
    song_attribute(year, Year), Year >= 2010,
    song_attribute(instruments, Inst),
    once((has_instrument(tabla, Inst); has_instrument(flute, Inst); has_instrument(sitar, Inst))),
    once((has_instrument(acoustic_guitar, Inst); has_instrument(bass, Inst); has_instrument(piano, Inst))).

recommend_genre('Modern Pop', 0.85, 'Modern (post-2015) song with an upbeat, acoustic pop feel.') :-
    song_attribute(year, Year), Year >= 2015,
    song_attribute(bpm, BPM), BPM >= 110,
    song_attribute(vocals, 'upbeat').


all_recommendations(Matches) :-
    findall(
        [Genre, Confidence, Reason],
        recommend_genre(Genre, Confidence, Reason),
        Matches
    ).


best_recommendation(Genre, Confidence, Reason) :-
    findall(
        conf(C, G, R),
        recommend_genre(G, C, R), 
        AllMatches
    ),
    \+ AllMatches = [],
    sort(1, @>=, AllMatches, [conf(Confidence, Genre, Reason)|_]).

has_instrument(Instrument, InstrumentList) :-
    member(Instrument, InstrumentList).