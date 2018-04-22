import { Pitch, NoteEnum, AccidentalEnum } from "../../../src/Common/DataObjects/Pitch";

describe("Pitch Unit Tests:", () => {
    describe("transpose Pitch", () => {
        let pitch: Pitch = new Pitch(NoteEnum.A, 1, AccidentalEnum.NONE);
        let transposedFundamentalAndOctave: {value: number; overflow: number; } =
          Pitch.CalculateTransposedHalfTone(pitch, 12);
        let higherTransposedFundamentalAndOctave: {value: number; overflow: number; } =
          Pitch.CalculateTransposedHalfTone(pitch, 26);

        it("should be 1 octave higher and same fundamental", (done: MochaDone) => {
            chai.expect(transposedFundamentalAndOctave.overflow).to.equal(1);
            chai.expect(transposedFundamentalAndOctave.value).to.equal(pitch.FundamentalNote);
            chai.expect(higherTransposedFundamentalAndOctave.overflow).to.equal(2);
            chai.expect(higherTransposedFundamentalAndOctave.value).to.equal(pitch.FundamentalNote + 2);
            done();
        });
    });

    describe("calculate Frequency from Pitch", () => {
        let pitch1: Pitch = new Pitch(NoteEnum.A, 1, AccidentalEnum.NONE);
        let pitch2: Pitch = new Pitch(NoteEnum.B, 1, AccidentalEnum.DOUBLEFLAT);
        let pitch3: Pitch = new Pitch(NoteEnum.G, 1, AccidentalEnum.DOUBLESHARP);

        let frequency1: number = Pitch.calcFrequency(Pitch.calcFractionalKey(pitch1.Frequency));
        let frequency2: number = Pitch.calcFrequency(Pitch.calcFractionalKey(pitch2.Frequency));
        let frequency3: number = Pitch.calcFrequency(Pitch.calcFractionalKey(pitch3.Frequency));

        it("should be 440Hz", (done: MochaDone) => {
            chai.expect(pitch1.Frequency).to.equal(440);
            chai.expect(pitch2.Frequency).to.equal(440);
            chai.expect(pitch3.Frequency).to.equal(440);
            chai.expect(frequency1).to.equal(440);
            chai.expect(frequency2).to.equal(440);
            chai.expect(frequency3).to.equal(440);
            done();
        });
    });

    describe("calculate fractional key", () => {
        // the values are validated against the C# output. TODO: ask mauz about the shift
        let pitch1: Pitch = new Pitch(NoteEnum.C, 6, AccidentalEnum.SHARP);   // C#6 -> 109
        let pitch2: Pitch = new Pitch(NoteEnum.B, 1, AccidentalEnum.NONE);    // B1 -> 59
        let pitch3: Pitch = new Pitch(NoteEnum.F, 4, AccidentalEnum.DOUBLEFLAT);  // Fbb4 -> 87
        let pitch4: Pitch = new Pitch(NoteEnum.E, -1, AccidentalEnum.DOUBLESHARP);    // E##-1 -> 30
        let pitch5: Pitch = new Pitch(NoteEnum.A, 1, AccidentalEnum.NONE);    // A1 -> 57

        let key1: number = Pitch.calcFractionalKey(pitch1.Frequency);
        let key2: number = Pitch.calcFractionalKey(pitch2.Frequency);
        let key3: number = Pitch.calcFractionalKey(pitch3.Frequency);
        let key4: number = Pitch.calcFractionalKey(pitch4.Frequency);
        let key5: number = Pitch.calcFractionalKey(pitch5.Frequency);

        it("pitch key should equal midi key", (done: MochaDone) => {
            chai.expect(key1).to.equal(109);
            chai.expect(key2).to.equal(59);
            chai.expect(key3).to.equal(87);
            chai.expect(key4).to.equal(30);
            chai.expect(key5).to.equal(57);
            done();
        });
    });

    describe("calculate Pitch from Frequency", () => {
        let octave: number = 1;
        let accidentals: number[] = [AccidentalEnum.DOUBLEFLAT,
            AccidentalEnum.FLAT,
            AccidentalEnum.NONE,
            AccidentalEnum.SHARP,
            AccidentalEnum.DOUBLESHARP,
        ];

        let pitch: Pitch;
        let calcedPitch: Pitch;

        for (let i: number = 0; i < Pitch.pitchEnumValues.length; i++) {
            for (let j: number = 0; j < accidentals.length; j++) {
                pitch = new Pitch(Pitch.pitchEnumValues[i], octave, accidentals[j]);
                calcedPitch = Pitch.fromFrequency(pitch.Frequency);

                it( "calcedPitch equals original, " +
                    `note: ${pitch.FundamentalNote}, octave: ${pitch.Octave}, accidental; ${pitch.Accidental}`,
                    (done: MochaDone) => {
                        // compare the frequencies here -> only AccidentalEnum None and Sharp will lead to same note, octave and accidental
                        chai.expect(pitch.Frequency).to.equal(calcedPitch.Frequency);
                        done();
                    });
            }
        }
    });

    describe("get Pitch from fractional key", () => {
        let octave: number = 5;
        let accidentals: number[] = [AccidentalEnum.DOUBLEFLAT,
            AccidentalEnum.FLAT,
            AccidentalEnum.NONE,
            AccidentalEnum.SHARP,
            AccidentalEnum.DOUBLESHARP,
        ];

        let pitch: Pitch;
        let calcedPitch: Pitch;

        for (let i: number = 0; i < Pitch.pitchEnumValues.length; i++) {
            for (let j: number = 0; j < accidentals.length; j++) {
                pitch = new Pitch(Pitch.pitchEnumValues[i], octave, accidentals[j]);
                let halftone: number = pitch.getHalfTone();
                calcedPitch = Pitch.fromHalftone(halftone);

                it( "calcedPitch equals original, " +
                    `note: ${pitch.FundamentalNote}, octave: ${pitch.Octave}, accidental; ${pitch.Accidental}`,
                    (done: MochaDone) => {
                        chai.expect(pitch.getHalfTone()).to.equal(calcedPitch.getHalfTone());
                        done();
                    });
            }
        }
    });

    // TODO: test ceiling and floor (needed for the music sheet transpose)
    // TODO: test getTransposedPitch (or delete it -> seems to be a less powerful implementation of CalculateTransposedHalfTone)
    // TODO: test DoEnharmonicEnchange (needed for the midi reader)
});
