package edu.ai;

import java.math.BigDecimal;
import java.util.Locale;
import java.util.Random;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

class AcceptanceTest {
    @ParameterizedTest(name="AC price {0} with {1} gives {2}")
    @CsvSource(value={
        "0.00|STUDENT10|0.00", "49.99|STUDENT10|49.99", "50.00|STUDENT10|45.00",
        "50.01|STUDENT10|45.01", "50.05|STUDENT10|45.04", "50.15|STUDENT10|45.13",
        "100.00|STUDENT10|90.00", "199.99|STUDENT10|179.99", "200.00|STUDENT10|180.00",
        "200.01|STUDENT10|180.01", "500.00|STUDENT10|480.00", "10000.00|STUDENT10|9980.00",
        "100.00|student10|90.00", "100.00|  student10  |90.00", "100.00|OTHER|100.00",
        "100.00|NULL|100.00", "100.00||100.00", "50.000|STUDENT10|45.00"
    }, delimiter='|', nullValues="NULL")
    void acceptance(String subtotal, String coupon, String expected) {
        assertEquals(new BigDecimal(expected), PriceCalculator.calculate(new BigDecimal(subtotal),coupon));
    }

    @ParameterizedTest(name="AC invalid subtotal {0}")
    @CsvSource({"-0.01", "10000.01", "50.001"})
    void rejectsInvalidSubtotal(String subtotal) {
        assertThrows(IllegalArgumentException.class, () -> PriceCalculator.calculate(new BigDecimal(subtotal),"STUDENT10"));
    }

    @Test void rejectsNullSubtotal() {
        assertThrows(IllegalArgumentException.class, () -> PriceCalculator.calculate(null,"STUDENT10"));
    }

    @Test void localeDoesNotChangeCouponMeaning() {
        Locale previous=Locale.getDefault();
        try {
            Locale.setDefault(Locale.forLanguageTag("tr-TR"));
            assertEquals(new BigDecimal("90.00"),PriceCalculator.calculate(new BigDecimal("100.00"),"student10"));
        } finally { Locale.setDefault(previous); }
    }

    @Test void integerCentsOracleAndInvariantsFor500Inputs() {
        Random random=new Random(20261012L);
        for (int i=0; i<500; i++) {
            long cents=random.nextInt(1000001);
            BigDecimal subtotal=BigDecimal.valueOf(cents,2);
            long discount=cents < 5000 ? 0 : Math.min((cents+5)/10,2000);
            BigDecimal actual=PriceCalculator.calculate(subtotal,"STUDENT10");
            assertEquals(BigDecimal.valueOf(cents-discount,2),actual,"cents="+cents);
            assertEquals(2,actual.scale());
            assertTrue(actual.signum() >= 0 && actual.compareTo(subtotal) <= 0);
            assertTrue(subtotal.subtract(actual).compareTo(new BigDecimal("20.00")) <= 0);
            assertEquals(subtotal,PriceCalculator.calculate(subtotal,"OTHER"));
        }
    }
}
