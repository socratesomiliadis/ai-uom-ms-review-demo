package edu.ai;
import java.math.BigDecimal;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.assertEquals;

class LegacyTest {
    @ParameterizedTest(name="legacy {0} with {1} gives {2}")
    @CsvSource({"40.00,STUDENT10,40.00", "100.00,STUDENT10,90.00", "100.00,OTHER,100.00"})
    void legacy(String subtotal, String coupon, String expected) {
        assertEquals(new BigDecimal(expected), PriceCalculator.calculate(new BigDecimal(subtotal),coupon));
    }
}
