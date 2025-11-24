import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 1

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "kahvi", 8)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)

        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called_with(
        "pekka",
        1,                # viite
        "12345",          # asiakkaan tili
        "33333-44455",    # kaupan tili
        5                 # hinta: vain yksi maito → 5 €
    )

        viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        for nimi in ["pekka", "matti", "liisa"]:
            self.kauppa.aloita_asiointi()
            self.kauppa.lisaa_koriin(1)
            self.kauppa.tilimaksu(nimi, "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

        self.pankki_mock.tilisiirto.assert_any_call("pekka", 1, "12345", "33333-44455", 5)
        self.pankki_mock.tilisiirto.assert_any_call("matti", 2, "12345", "33333-44455", 5)
        self.pankki_mock.tilisiirto.assert_any_call("liisa", 3, "12345", "33333-44455", 5)

