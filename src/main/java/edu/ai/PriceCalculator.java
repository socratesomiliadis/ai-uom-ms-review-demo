package edu.ai;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Locale;

public final class PriceCalculator {
    private PriceCalculator() {}

    public static BigDecimal calculate(BigDecimal subtotal, String coupon) {
        if (subtotal == null || subtotal.signum() < 0
                || subtotal.compareTo(new BigDecimal("10000")) > 0
                || subtotal.stripTrailingZeros().scale() > 2) {
            throw new IllegalArgumentException("Invalid subtotal");
        }
        String code = coupon == null ? "" : coupon.strip().toUpperCase(Locale.ROOT);
        if ("STUDENT10".equals(code) && subtotal.compareTo(new BigDecimal("50")) >= 0) {
            BigDecimal discount = subtotal.multiply(new BigDecimal("0.10"))
                    .min(new BigDecimal("20")).setScale(2, RoundingMode.HALF_UP);
            return subtotal.subtract(discount).setScale(2, RoundingMode.HALF_UP);
        }
        return subtotal.setScale(2, RoundingMode.UNNECESSARY);
    }
}
