# Seq2seq models for decoding the Enigma machine

The [Enigma machine](https://brilliant.org/wiki/enigma-machine/) was designed by Germans during WWII so they could communicate via encrypted messages. Alan Turing and others were able to design a decoder to crack the encryption and intercept messages. Here, we've created two seq2seq models to decode the enigma machine: RNN with attention, and a transformer.

The RNN scored around 93% accuracy and the transformer around 98% on new data. If 80% of the characters in a sequence are successfully able to be decoded to its proper value, I mark it as correct since, if a human was reading it, they'd likely be able to unscramble the rest. One caveat is that inference is fairly slow. On a standard laptop, it takes about 3 minutes to run inference on 100 samples for the transformer and 1 minute for the RNN. Depending on the application, training smaller models should increase the inference speed with some trade-off for accuracy. These models were trained using Google Colab which is a great tool that gives you free access to a GPU.

Any feedback is welcome in the form of issues/PRs!
