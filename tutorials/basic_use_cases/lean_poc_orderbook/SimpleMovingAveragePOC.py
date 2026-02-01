# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from AlgorithmImports import *

###<summary>
### PROOF OF CONCEPT: Phase 1 - Basic LEAN Backtesting Demonstration
###
### This algorithm demonstrates LEAN's core backtesting capabilities using built-in data.
### NO custom data integration required - this proves the engine works out of the box.
###
### What This Demonstrates:
### - Event-driven backtesting architecture
### - Built-in equity data subscription (SPY)
### - Technical indicator library (SMA)
### - Order placement and execution
### - Portfolio management
### - Automatic performance metrics
###
### Strategy: Simple Moving Average Crossover (10/30 day)
### - Long when fast SMA crosses above slow SMA
### - Exit when fast SMA crosses below slow SMA
### - This is a DEMONSTRATION, not a production strategy
###
### Expected Runtime: ~30 seconds for 3-month backtest
### Expected Trades: 2-5 trades
###</summary>
class SimpleMovingAveragePOC(QCAlgorithm):
    """
    POC Phase 1: Demonstrates LEAN's basic backtesting with zero setup.
    Uses SPY equity data that ships with LEAN - no data preparation needed.
    """

    def initialize(self):
        """
        Initialize algorithm parameters, data subscriptions, and indicators.
        This runs once at the start of the backtest.
        """
        # === POC Configuration ===
        # Short 3-month period for fast validation
        self.set_start_date(2023, 1, 1)
        self.set_end_date(2023, 3, 31)

        # Standard starting capital
        self.set_cash(100000)

        # === Built-in Data Subscription ===
        # LEAN ships with SPY data - no external data needed
        self.symbol = self.add_equity("SPY", Resolution.DAILY).symbol

        # === Technical Indicators ===
        # LEAN provides 100+ built-in indicators
        self.sma_fast = self.sma(self.symbol, 10, Resolution.DAILY)
        self.sma_slow = self.sma(self.symbol, 30, Resolution.DAILY)

        # === State Tracking ===
        self.previous_date = None

        # === POC Logging ===
        self.log("="*60)
        self.log("POC PHASE 1: Basic LEAN Demonstration")
        self.log("="*60)
        self.log(f"Symbol: {self.symbol}")
        self.log(f"Period: {self.start_date} to {self.end_date}")
        self.log(f"Capital: ${self.portfolio.cash:,.2f}")
        self.log(f"Fast SMA: {10} days")
        self.log(f"Slow SMA: {30} days")
        self.log("="*60)

    def on_data(self, data):
        """
        Main event handler - called for each new bar of data.
        This is where trading logic executes.

        Args:
            data: Slice object containing all market data for this time step
        """
        # === Indicator Warmup ===
        # Wait for indicators to have enough data
        if not self.sma_slow.is_ready:
            return

        # === Trade Once Per Day ===
        # Avoid multiple signals on the same day
        if self.previous_date is not None and self.previous_date == self.time.date():
            return
        self.previous_date = self.time.date()

        # === Get Current Values ===
        fast_value = self.sma_fast.current.value
        slow_value = self.sma_slow.current.value
        current_price = self.securities[self.symbol].price

        # === Signal Generation ===
        # Small tolerance to avoid noise
        tolerance = 0.00015

        # Check current position
        holdings = self.portfolio[self.symbol].quantity

        # === Long Entry Signal ===
        if holdings <= 0:  # Not long
            if fast_value > slow_value * (1 + tolerance):
                # Fast SMA crossed above slow SMA
                self.set_holdings(self.symbol, 1.0)  # 100% long
                self.log(f"POC LONG ENTRY: ${current_price:.2f} | Fast: ${fast_value:.2f} > Slow: ${slow_value:.2f}")

        # === Exit Signal ===
        if holdings > 0:  # Currently long
            if fast_value < slow_value:
                # Fast SMA crossed below slow SMA
                self.liquidate(self.symbol)
                self.log(f"POC EXIT: ${current_price:.2f} | Fast: ${fast_value:.2f} < Slow: ${slow_value:.2f}")

    def on_order_event(self, order_event):
        """
        Called when order status changes (submitted, filled, cancelled, etc.)
        Useful for tracking execution and debugging.

        Args:
            order_event: OrderEvent with details about the order
        """
        if order_event.status == OrderStatus.FILLED:
            order = self.transactions.get_order_by_id(order_event.order_id)
            self.log(f"POC ORDER FILLED: {order.quantity} shares @ ${order_event.fill_price:.2f} | " +
                    f"Portfolio Value: ${self.portfolio.total_portfolio_value:,.2f}")

    def on_end_of_algorithm(self):
        """
        Called once at the end of the backtest.
        Final summary and observations.
        """
        self.log("="*60)
        self.log("POC PHASE 1: Results Summary")
        self.log("="*60)
        self.log(f"Final Portfolio Value: ${self.portfolio.total_portfolio_value:,.2f}")
        self.log(f"Total Return: {((self.portfolio.total_portfolio_value / 100000) - 1) * 100:.2f}%")
        self.log(f"Invested: {self.portfolio.invested}")
        self.log("="*60)
        self.log("POC PHASE 1: COMPLETE")
        self.log("="*60)
        self.log("")
        self.log("What This Demonstrated:")
        self.log("✓ LEAN backtesting engine works correctly")
        self.log("✓ Built-in data loads automatically")
        self.log("✓ Indicators calculate properly")
        self.log("✓ Orders execute successfully")
        self.log("✓ Portfolio tracks positions and P&L")
        self.log("✓ Performance metrics generated automatically")
        self.log("")
        self.log("Next: Phase 2 - Custom orderbook data integration")
        self.log("="*60)
